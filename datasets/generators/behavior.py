
import random

ROLE_BEHAVIOR = {
    "DOCTOR": {
        "view_records": (2, 8),
        "update_probability": 0.75,
        "print_probability": 0.30,
        "download_probability": 0.05,
    },

    "NURSE": {
        "view_records": (1, 5),
        "update_probability": 0.60,
        "print_probability": 0.10,
        "download_probability": 0.02,
    },

    "RADIOLOGIST": {
        "view_records": (3, 10),
        "update_probability": 0.10,
        "print_probability": 0.80,
        "download_probability": 0.01,
    },

    "LAB_TECHNICIAN": {
        "view_records": (2, 6),
        "update_probability": 0.25,
        "print_probability": 0.05,
        "download_probability": 0.01,
    },

    "ADMIN": {
        "view_records": (0, 2),
        "update_probability": 0.10,
        "print_probability": 0.00,
        "download_probability": 0.00,
    },
}

WORKING_HOURS = {
    "DOCTOR": (7, 18),
    "NURSE": (0, 23),
    "RADIOLOGIST": (8, 17),
    "LAB_TECHNICIAN": (7, 19),
    "ADMIN": (9, 17),
}

def generate_workflow(role):
    """
    Generate a realistic workflow for a user based on their role.
    """

    profile = ROLE_BEHAVIOR[role]

    workflow = ["LOGIN"]

    # Number of patient records viewed
    num_views = random.randint(*profile["view_records"])

    workflow.extend(["VIEW_RECORD"] * num_views)

    # Maybe update a record
    if random.random() < profile["update_probability"]:
        workflow.append("UPDATE_RECORD")

    # Maybe print
    if random.random() < profile["print_probability"]:
        workflow.append("PRINT_RECORD")

    # Maybe download
    if random.random() < profile["download_probability"]:
        workflow.append("DOWNLOAD_RECORD")

    workflow.append("LOGOUT")

    return workflow