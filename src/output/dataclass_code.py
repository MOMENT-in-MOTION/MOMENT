# --- GENERATED CODE - DO NOT EDIT ---
from dataclasses import dataclass, field
from __future__ import annotations
from enum_code import *

@dataclass
class Person:
        name : str
        age : int
        isActive : bool | None
        address : Address
        manager : Person | None
        projects : list[Project]


@dataclass
class Address:
        street : str
        city : str
        zipCode : int | None


@dataclass
class Project:
        title : str
        priority : int
        status : Status
        tasks : list[Task]


@dataclass
class Task:
        description : str
        estimatedHours : int | None
        completed : bool


@dataclass
class Department:
        name : str
        budget : list[int]
        employees : list[Person]


