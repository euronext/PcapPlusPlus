import pytest

def pytest_addoption(parser):
	parser.addoption("--interface", action="store", help="interface IP address or name.")
	parser.addoption("--gateway", action="store", help="default gateway IP address.")

@pytest.fixture
def interface_ip_name(request):
	return request.config.getoption("--interface")

@pytest.fixture
def gateway_ip(request):
	return request.config.getoption("--gateway")

def pytest_configure(config):
	config.addinivalue_line("markers", "interface_needed: mark test as need interface IP or name from command line")
	config.addinivalue_line("markers", "gateway_ip_needed: mark test as need default gateway IP from command line")


def pytest_collection_modifyitems(config, items):
	if not config.getoption("--interface"):
		skip_no_interface = pytest.mark.skip(reason="need --interface option to run")
		for item in items:
			if "interface_needed" in item.keywords:
				item.add_marker(skip_no_interface)

	if not config.getoption("--gateway"):
		skip_no_gateway = pytest.mark.skip(reason="need --gateway option to run")
		for item in items:
			if "gateway_ip_needed" in item.keywords:
				item.add_marker(skip_no_gateway)