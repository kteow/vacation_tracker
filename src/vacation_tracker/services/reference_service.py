from repositories import department_repository, vacation_type_repository

def get_departments():
    return department_repository.get_all()

def get_vacation_types():
    return vacation_type_repository.get_all()