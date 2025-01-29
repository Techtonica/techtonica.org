import pandas as pd

users = [
    {
        "first_name": "Suzanne",
        "last_name": "Collins",
        "email": "suzanne@example.com",
        "wpm": 45,
        "freecodecamp": True,
        "references": 1,
        "income_eligible": False,
        "gender": "Woman",
        "computer_literate": True,
        "stable_housing": True,
        "no_recent_bootcamp": True,
        "eligibility_score": 70,
    },
    {
        "first_name": "Stephen",
        "last_name": "King",
        "email": "stephen@example.com",
        "wpm": 55,
        "freecodecamp": False,
        "references": 2,
        "income_eligible": False,
        "gender": "Man",
        "computer_literate": True,
        "stable_housing": True,
        "no_recent_bootcamp": True,
        "eligibility_score": 65,
    },
    {
        "first_name": "Shirley",
        "last_name": "Jackson",
        "email": "shirley@example.com",
        "wpm": 40,
        "freecodecamp": True,
        "references": 1,
        "income_eligible": True,
        "gender": "woman",
        "computer_literate": False,
        "stable_housing": True,
        "no_recent_bootcamp": True,
        "eligibility_score": 60,
    },
    {
        "first_name": "Ernest",
        "last_name": "Hemingway",
        "email": "ernest@example.com",
        "wpm": 60,
        "freecodecamp": False,
        "references": 1,
        "income_eligible": False,
        "gender": "man",
        "computer_literate": False,
        "stable_housing": True,
        "no_recent_bootcamp": False,
        "eligibility_score": 50,
    },
]

application_status = [
    {
        "user_id": 0,
        "submitted": True,
        "screening": True,
        "workshop": True,
        "pair_programming": True,
        "take_home_code": True,
        "staff_interview": True,
        "board_interview": True,
        "reference_submitted": True,
        "financial": True,
        "pending": True,
        "approved": False,
        "prescreen_rejected": False,
        "rejected": False,
    },
    {
        "user_id": 1,
        "submitted": False,
        "screening": False,
        "workshop": False,
        "pair_programming": False,
        "take_home_code": False,
        "staff_interview": False,
        "board_interview": False,
        "reference_submitted": False,
        "financial": False,
        "pending": True,
        "approved": False,
        "prescreen_rejected": False,
        "rejected": False,
    },
    {
        "user_id": 2,
        "submitted": True,
        "screening": True,
        "workshop": True,
        "pair_programming": False,
        "take_home_code": False,
        "staff_interview": False,
        "board_interview": False,
        "reference_submitted": True,
        "financial": True,
        "pending": True,
        "approved": False,
        "prescreen_rejected": False,
        "rejected": False,
    },
    {
        "user_id": 3,
        "submitted": True,
        "screening": True,
        "workshop": True,
        "pair_programming": False,
        "take_home_code": False,
        "staff_interview": True,
        "board_interview": False,
        "reference_submitted": True,
        "financial": True,
        "pending": True,
        "approved": False,
        "prescreen_rejected": False,
        "rejected": False,
    },
]

user_df = pd.DataFrame(users)
app_df = pd.DataFrame(application_status)


def user(id):
    return user_df.loc[id]


def users():
    return user_df


def application(id):
    return user_df.join(app_df.set_index("user_id")).loc[id]


def applications():
    return user_df.join(app_df.set_index("user_id"))


def total_users():
    return len(user_df)


def total_apps():
    return len(app_df)


def total_submitted():
    return len(app_df.loc[app_df["submitted"]])


def total_workshop():
    return len(app_df.loc[app_df["workshop"]])


def test_data():
    print("User with id 0: {user}".format(user=user(0)))
    print("All users:")
    print(users())
    print("Application with id 0: {app}".format(app=application(0)))
    print("All applications:")
    print(applications())
    print("# of users: {x}".format(x=total_users()))
    print("# of applications: {x}".format(x=total_apps()))
    print("# of submitted applications: {x}".format(x=total_submitted()))
    print("# of applicants to attend workshop: {x}".format(x=total_workshop()))


test_data()
