from sqlalchemy.orm import Session
from typing import Any
from . import schemas, models


# using this function for avoid code-duplication
# because sqlalchemy-orm models are not created manually, but just synchronized with existing tables

def create_db_instance(db: Session, cls_name: str, **kwargs) -> Any:
	try:
		cls = getattr(models, cls_name.title())
	except Exception:
		raise AttributeError("Model isn't defined at 'models.py'")
	db_obj = cls(
		**kwargs
	)
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)
	db.close()
	return db_obj


