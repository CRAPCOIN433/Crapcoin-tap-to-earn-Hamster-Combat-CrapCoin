import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from bot.database.base import Base


class TaskType(Enum):
    DAILY = "daily"
    TAP = "tap"
    REFERRAL = "referral"
    LEVEL_UP = "level_up"


class User(Base):
    __tablename__ = "users"
    
    # Идентификаторы
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    # Игровые данные
    balance = Column(Integer, default=0, nullable=False)
    total_earned = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    tap_power = Column(Integer, default=1, nullable=False)
    tap_multiplier = Column(Float, default=1.0, nullable=False)
    
    # Статистика
    total_taps = Column(Integer, default=0, nullable=False)
    last_daily_claim = Column(DateTime, nullable=True)
    last_tap = Column(DateTime, nullable=True)
    
    # Реферальная система
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    referred_users = relationship('User', foreign_keys=[referrer_id])
    
    # Служебная информация
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User {self.telegram_id} - {self.username}>"
    
    @property
    def full_name(self) -> str:
        """Получить полное имя пользователя."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username or "Безымянный пользователь"
    
    @property
    def can_tap(self) -> bool:
        """Проверка возможности нажать на кнопку тапа."""
        if not self.last_tap:
            return True
        
        from bot.config import load_config
        config = load_config()
        cooldown = datetime.timedelta(seconds=config.bot.tap_cooldown_seconds)
        return datetime.datetime.now() > self.last_tap + cooldown
    
    @property
    def time_to_next_tap(self) -> Optional[datetime.timedelta]:
        """Время до следующей возможности нажать на кнопку."""
        if self.can_tap or not self.last_tap:
            return None
        
        from bot.config import load_config
        config = load_config()
        cooldown = datetime.timedelta(seconds=config.bot.tap_cooldown_seconds)
        remaining = (self.last_tap + cooldown) - datetime.datetime.now()
        return remaining if remaining.total_seconds() > 0 else None
    
    @property
    def can_claim_daily(self) -> bool:
        """Проверка возможности получить ежедневный бонус."""
        if not self.last_daily_claim:
            return True
        
        today = datetime.datetime.now().date()
        return self.last_daily_claim.date() < today


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    type = Column(String(50), nullable=False)
    reward = Column(Integer, nullable=False)
    target_count = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Task {self.id} - {self.title}>"


class UserTask(Base):
    __tablename__ = "user_tasks"
    
    id = Column(Integer,