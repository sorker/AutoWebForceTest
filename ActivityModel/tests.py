from django.test import TestCase
import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from AutoActivity.services import sshConnect, sshClose, allTask


if __name__ in "__main__":
    service = sshConnect('192.168.94.131', 'root', '123456', '22')
    args = allTask(service)
    print(args)
    TestService.objects.create(site_ip='192.168.50.243', time_data=str(args))
    sshClose(service)
