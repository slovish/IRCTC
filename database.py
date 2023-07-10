from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



USER_SQLALCEMY_DB_URL = "mysql+pymysql://root:Vishal#16@localhost:3306/user_data"
# Train_SQLALCEMY_DB_URL = "mysql+pymysql://root:Vishal#16@localhost:3306/train_data"

userDbEngine = create_engine(USER_SQLALCEMY_DB_URL)
userDbSessionLocal = sessionmaker(autocommit = False, bind = userDbEngine)

# trainDbEngine = create_engine(Train_SQLALCEMY_DB_URL)
# trainDbSessionLocal = sessionmaker(autocommit = False, bind = trainDbEngine)

userBase = declarative_base()
# trainBase = declarative_base()

