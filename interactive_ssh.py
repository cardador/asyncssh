import asyncio, asyncssh, sys
import logging

PROMPT = r':~$'


class Target:

    async def _run_client(self, cmdsequence, ip, **kwargs):
        async with asyncssh.connect(ip, **kwargs) as conn:
            chan, session = await conn.create_session(
                asyncssh.SSHClientProcess,
                # next line should point to an interactive (slow in my case)
                # process on a remote host'
                command='<remote process, eg: bc>')
            await asyncio.wait_for(session.stdout.readuntil(PROMPT), timeout=10)
            for cmd in cmdsequence:
                chan.write(cmd + '\n')
                result = ''
                try:
                    result+=await\
                            asyncio.wait_for(
                                session.stdout.readuntil(PROMPT),timeout=10)
                except Exception as e:
                    logging.warning("prompt timeout step {}".format(e))
                print(result, end='')

    def remote_cmd(self, cmdsequence, ip, user):
        try:
            asyncio.get_event_loop().run_until_complete(
                self._run_client(cmdsequence, ip, user))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))


tg = Target()
tg.remote_cmd(['2+2', '1*2*3*4', '2^32'], '192.168.0.100', username='<user>')
