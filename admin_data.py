import pandas as pd

users = [
    {"firstname": "Suzanne", "lastname": "Collins"},
    {"firstname": "Stephen", "lastname": "King"},
    {"firstname": "Shirley", "lastname": "Jackson"},
    {"firstname": "Ernest", "lastname": "Hemingway"},
]

applications = [
    {"user_id": 0, "submitted": True, "workshop": True},
    {"user_id": 1, "submitted": False, "workshop": False},
    {"user_id": 2, "submitted": True, "workshop": False},
    {"user_id": 3, "submitted": True, "workshop": False},
    {"user_id": 3, "submitted": False, "workshop": False},
]

user_df = pd.DataFrame(users)
app_df = pd.DataFrame(applications)


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
