# ORM模型定义 
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    year = Column(Integer, nullable=True)

class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, index=True)
    uci_code = Column(String(50), unique=True, nullable=False, comment="UCI编号")
    name = Column(String(200), nullable=False, comment="车队名称")
    country = Column(String(100), nullable=False, comment="国家")
    founded_year = Column(Integer, nullable=True, comment="成立年份")
    sponsor = Column(String(200), nullable=True, comment="赞助商")
    former_names = Column(String(500), nullable=True, comment="历史名称")
    note = Column(String(500), nullable=True, comment="备注")

class Rider(Base):
    __tablename__ = "rider"
    id = Column(Integer, primary_key=True, index=True)
    name_cn = Column(String(100), nullable=False, comment="姓名中文")
    name_en = Column(String(100), nullable=True, comment="姓名英文")
    age = Column(Integer, nullable=True, comment="年龄")
    birth_date = Column(String(20), nullable=True, comment="出生年月")
    current_team_id = Column(Integer, ForeignKey("team.id"), nullable=True, comment="现在服役车队")
    former_teams = Column(String(500), nullable=True, comment="曾经服役车队")
    rider_type = Column(String(100), nullable=True, comment="车手类型")
    achievements = Column(String(1000), nullable=True, comment="车手成就")
    note = Column(String(500), nullable=True, comment="备注")
    nationality = Column(String(100), nullable=True, comment="国籍")
    gender = Column(String(20), nullable=True, comment="性别")
    uci_id = Column(String(50), nullable=True, comment="UCI注册编号")

    team = relationship("Team", backref="riders") 