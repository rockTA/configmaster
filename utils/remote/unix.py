from utils.remote import common


class UnixRemoteControl(common.NetworkDeviceRemoteControl):
    def __init__(self, *args, **kwargs):
        super(UnixRemoteControl, self).__init__(*args, **kwargs)
        self.allocate_pty = True

    def expect_prompt(self):
        self.interact.expect(r'.*?~#')

    def change_admin_password(self, new_password, verify=True):
        self.interact.send('passwd')
        self.interact.expect('Enter new UNIX password: ')
        self.interact.send(new_password)
        self.interact.expect('Retype new UNIX password: ')
        self.interact.send(new_password)
        self.interact.expect('passwd: .*')
        output = self.interact.current_output_clean.strip().split('\n')[0]

        if not "password updated successfully" in output:
            raise common.OperationalError(
                'Password change failed: "%s"' % output)

        if verify:
            if not self.verify_login(self.username, new_password):
                raise common.OperationalError(
                    "Password change verification failed")

        return output

    def get_raw_time(self):
        raise NotImplementedError


if __name__ == '__main__':
    rc = UnixRemoteControl("unix.continum.net", timeout=5)
    rc.connect("root", "foobar")
    # rc.connect("root", getpass.getpass())

    print repr(rc.change_admin_password('foobar'))
