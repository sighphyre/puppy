from random import randint, choice
from string import ascii_letters, digits
from json import dumps


def random_string(length=10):
    return "".join(choice(ascii_letters + digits) for _ in range(length))


def generate_default():
    return {
        "name": "default",
        "parameters": {},
    }


def generate_user_with_id():
    user_ids = [str(x) for x in range(1, randint(2, 100))]
    return {
        "name": "userWithId",
        "parameters": {
            "userIds": user_ids,
        },
    }


def generate_gradual_rollout_user_id():
    return {
        "name": "gradualRolloutUserId",
        "parameters": {
            "percentage": str(randint(0, 100)),
            "groupId": random_string(10),
        },
    }


def generate_gradual_rollout_random():
    return {
        "name": "gradualRolloutRandom",
        "parameters": {"percentage": str(randint(0, 100))},
    }


def generate_gradual_rollout_session_id():
    return {
        "name": "gradualRolloutSessionId",
        "parameters": {
            "percentage": str(randint(0, 100)),
            "groupId": random_string(10),
        },
    }


def generate_remote_address():
    ip_addresses = ",".join(
        [
            f"{randint(1, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"
            for _ in range(10)
        ]
    )
    return {
        "name": "remoteAddress",
        "parameters": {"IPs": ip_addresses},
    }


def generate_flexible_rollout():
    return {
        "name": "flexibleRollout",
        "parameters": {
            "rollout": str(randint(0, 100)),
            "stickiness": "default",  ## do we care here? Probably not right now
            "groupId": random_string(10),
        },
    }


VALID_STRATEGIES = {
    "default": generate_default,
    "userWithId": generate_user_with_id,
    "gradualRolloutUserId": generate_gradual_rollout_user_id,
    "gradualRolloutRandom": generate_gradual_rollout_random,
    "gradualRolloutSessionId": generate_gradual_rollout_session_id,
    "remoteAddress": generate_remote_address,
    "flexibleRollout": generate_flexible_rollout,
}


def gen_date():
    year = randint(2000, 2023)
    month = randint(1, 12)
    day = randint(1, 28)  # To avoid issues with month-end days
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}.000Z"


def gen_semver():
    return f"{randint(1, 3)}.{randint(0, 9)}.{randint(0, 9)}"


def create_constraint_gen(operator, value_gen):
    def constraint_gen():
        return {
            "contextName": "version",
            "operator": operator,
            "value": value_gen(),
        }

    return constraint_gen


VALID_CONSTRAINTS = {
    "STR_STARTS_WITH": create_constraint_gen("STR_STARTS_WITH", random_string),
    "STR_ENDS_WITH": create_constraint_gen("STR_ENDS_WITH", random_string),
    "STR_CONTAINS": create_constraint_gen("STR_CONTAINS", random_string),
    "NUM_EQ": create_constraint_gen("NUM_EQ", lambda: str(randint(0, 100))),
    "NUM_GT": create_constraint_gen("NUM_GT", lambda: str(randint(0, 100))),
    "NUM_GTE": create_constraint_gen("NUM_GTE", lambda: str(randint(0, 100))),
    "NUM_LT": create_constraint_gen("NUM_LT", lambda: str(randint(0, 100))),
    "NUM_LTE": create_constraint_gen("NUM_LTE", lambda: str(randint(0, 100))),
    "DATE_AFTER": create_constraint_gen("DATE_AFTER", gen_date),
    "DATE_BEFORE": create_constraint_gen("DATE_BEFORE", gen_date),
    "SEMVER_EQ": create_constraint_gen("SEMVER_EQ", gen_semver),
    "SEMVER_GT": create_constraint_gen("SEMVER_GT", gen_semver),
    "SEMVER_LT": create_constraint_gen("SEMVER_LT", gen_semver),
}


def gen_random_constraint():
    constraint_name = choice(list(VALID_CONSTRAINTS.keys()))
    return VALID_CONSTRAINTS[constraint_name]()


def gen_random_strategy():
    strategy_name = choice(list(VALID_STRATEGIES.keys()))
    strategy = VALID_STRATEGIES[strategy_name]()
    strategy["constraints"] = [gen_random_constraint() for _ in range(randint(0, 3))]
    return strategy


def generate_random_feature(name_len=10):
    feature_name = "F" + "".join(
        choice(ascii_letters + digits) for _ in range(name_len)
    )

    return {
        "name": feature_name,
        "enabled": True,
        "description:": f"{feature_name} description",
        "strategies": [gen_random_strategy() for _ in range(randint(1, 3))],
    }


def generate_feature_set(min=100, max=1000):
    return {
        "features": [generate_random_feature() for _ in range(randint(min, max))],
        "version": 2,
    }

if __name__ == "__main__":
    feature_set = generate_feature_set()
    print(dumps(feature_set))
    # print("Generated feature set with", len(feature_set["features"]), "features.")