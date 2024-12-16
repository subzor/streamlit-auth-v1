from dataclasses import dataclass


@dataclass
class UserDetails:
    id: int
    email: str
    name: str
    username: str
    password: str
    role: str