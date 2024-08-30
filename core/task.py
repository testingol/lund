import requests

from smart_airdrop_claimer import base
from core.headers import headers


def check_in(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.text
        return data
    except:
        return None


def process_check_in(token, proxies=None):
    status = check_in(token=token, proxies=proxies)
    if status == "OK":
        base.log(f"{base.white}Auto Check-in: {base.green}Success")
    elif "same day" in status:
        base.log(f"{base.white}Auto Check-in: {base.red}Checked in already")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Fail")


def get_task(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/tasks"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def start_task(token, task_id, proxies=None):
    url = f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/start"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        return data
    except:
        return None


def claim_task(token, task_id, proxies=None):
    url = f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim"
    payload = {}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["status"]
        return status
    except:
        return None


def do_task(token, task_id, task_name, task_status, proxies=None):
    if task_status == "FINISHED":
        base.log(f"{base.white}{task_name}: {base.green}Completed")
    elif task_status == "READY_FOR_CLAIM":
        claim_task_status = claim_task(token=token, task_id=task_id, proxies=proxies)
        if claim_task_status == "FINISHED":
            base.log(f"{base.white}{task_name}: {base.green}Claim Success")
        else:
            base.log(f"{base.white}{task_name}: {base.red}Claim Fail")
    elif task_status == "NOT_STARTED":
        start = start_task(token=token, task_id=task_id, proxies=proxies)
        try:
            status = start["status"]
            if status == "STARTED":
                base.log(f"{base.white}{task_name}: {base.green}Start Success")
            else:
                base.log(f"{base.white}{task_name}: {base.red}Start Fail")
        except:
            message = start["message"]
            base.log(f"{base.white}{task_name}: {base.red}{message}")
    elif task_status == "STARTED":
        base.log(f"{base.white}{task_name}: {base.red}Started but not ready to claim")
    else:
        base.log(f"{base.white}{task_name}: {base.red}Unknown Status - {task_status}")


def process_do_task(token, proxies=None):
    task_list = get_task(token=token, proxies=proxies)
    for task_group in task_list:
        group = task_group["title"]
        tasks = task_group["tasks"]
        base.log(f"{base.white}Task Group: {base.yellow}{group}")
        for task in tasks:
            if "subTasks" in task.keys():
                sub_tasks = task["subTasks"]
                for sub_task in sub_tasks:
                    task_id = sub_task["id"]
                    task_name = sub_task["title"]
                    task_status = sub_task["status"]
                    do_task(
                        token=token,
                        task_id=task_id,
                        task_name=task_name,
                        task_status=task_status,
                        proxies=proxies,
                    )
                task_id = task["id"]
                task_name = task["title"]
                task_status = task["status"]
                do_task(
                    token=token,
                    task_id=task_id,
                    task_name=task_name,
                    task_status=task_status,
                    proxies=proxies,
                )
            else:
                task_id = task["id"]
                task_name = task["title"]
                task_status = task["status"]
                do_task(
                    token=token,
                    task_id=task_id,
                    task_name=task_name,
                    task_status=task_status,
                    proxies=proxies,
                )


def claim_ref(token, proxies=None):
    url = "https://gateway.blum.codes/v1/friends/claim"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_claim_ref(token, proxies=None):
    status = claim_ref(token=token, proxies=proxies)
    try:
        claim_balance = float(status["claimBalance"])
        base.log(
            f"{base.white}Auto Claim Ref: {base.green}Success | Added {claim_balance:,} points"
        )
    except:
        message = status["message"]
        base.log(f"{base.white}Auto Claim Ref: {base.red}{message}")
