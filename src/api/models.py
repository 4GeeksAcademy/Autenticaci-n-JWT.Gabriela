from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask.bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    def set_password(self, password: str):
        """Genera el hash a partir de la contraseña en texto plano."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica si la contraseña ingresada coincide con el hash guardado."""
        return check_password_hash(self.password_hash, password)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }