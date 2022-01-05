# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from ncs.dp import Action


import _ncs
import paramiko


# ---------------
# ACTIONS EXAMPLE
# ---------------
class ExecAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.device: ', input.device)
        self.log.info('action input.command: ', input.command)

        with ncs.maapi.single_read_trans('admin', 'python') as t:
          root = ncs.maagic.get_root(t)
          device = root.devices.device[input.device]
          username = root.devices.authgroups.group[device.authgroup].default_map.remote_name
          secret = root.devices.authgroups.group[device.authgroup].default_map.remote_password

          self.log.info('action address: ', device.address)
          self.log.info('action username: ', username)
          self.log.info('action encrypted password: ', secret)

          # decpyt password
          m = ncs.maapi.Maapi()
          m.install_crypto_keys()
          password = _ncs.decrypt(secret)
          self.log.info('action password: ', password)

          # get ssh hostkey
          algorithm = None
          for key in device.ssh.host_key.keys():
            algorithm = key 
            break
            
          self.log.info('action host_key algorithm: ', str(algorithm))

          if str(algorithm) == '{ssh-rsa}':
            key = paramiko.RSAKey(data=device.ssh.host_key[algorithm].key_data)
          elif str(algorithm) == '{ssh-dss}':
            key = paramiko.DSSKey(data=device.ssh.host_key[algorithm].key_data)
          else:
            output.result = "invalid ssh algorithm: " + str(algorithm)
            return

          # connect SSH
          client = paramiko.SSHClient()
          client.get_host_keys().add(device.address, algorithm, key)
          client.connect(device.address, 22, username, password, allow_agent=False, look_for_keys=False)
    
          # run command
          stdin, stdout, stderr = client.exec_command(input.command)

          # Updating the output data structure will result in a response being returned to the caller.
          output.result = stdout.read().decode("utf-8")
          self.log.info('action result:\n', output.result)

          return

        # error
        output.result = "can't get maapi session"
        return

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # When using actions, this is how we register them:
        #
        self.register_action('py_cli-action', ExecAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
