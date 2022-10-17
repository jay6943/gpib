import thorlabs_apt as apt

apt.list_available_devices()
stage = apt.Motor(45151484)

print('ok')
stage.move_to(65)