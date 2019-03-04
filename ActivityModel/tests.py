from django.test import TestCase
import django
import os
import time
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from AutoActivity.services import sshConnect, sshClose, allTask


if __name__ in "__main__":
    service = sshConnect('192.168.94.133', 'root', '123456', '22')
    time_sl = 0
    while time_sl <= 10:
        args = allTask(service)
        print(args)
        TestService.objects.create(site_ip='192.168.94.133', time_data=str(args))
        time.sleep(5)
        time_sl += 5
    sshClose(service)
    test_services = TestService.objects.values()
    for test_service in test_services:
        b = test_service.get('time_data').replace('\'', '\"')
        print(b)
        a = json.loads(b)
        print("=", a)
        print(type(a))
