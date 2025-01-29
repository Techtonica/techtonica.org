import pandas as pd

applications = [
    {"user_id": 0, "submitted": True, "workshop": True},
    {"user_id": 1, "submitted": False, "workshop": False},
    {"user_id": 2, "submitted": True, "workshop": False},
    {"user_id": 3, "submitted": True, "workshop": False},
]

df = pd.DataFrame(applications)


def users(id):
    return df.loc[id]


def total_apps():
    return len(df)


def total_submitted():
    return len(df.loc[df["submitted"]])


def total_workshop():
    return len(df.loc[df["workshop"]])


def test_data():
    print("Number of users: {x}".format(x=total_apps()))
    print("# of submitted applications: {x}".format(x=total_submitted()))
    print("# of applicants to attend workshop: {x}".format(x=total_workshop()))


test_data()
