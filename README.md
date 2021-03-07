# evennia-alexa
![img](https://img.shields.io/badge/build-alpha-yellow) Feel free to steal this code, but don't trust it.

```
Example objects.py

    def msg(self, text=None, **kwargs):
        """
        Generates an Alexa-compatible response, then disconnects the session.
        Replaces self.msg, to some degree. If no text= is passed, it tries to recreate
        it from onscreen_primary, onscreen_secondary, onscreen_tertiary. If that fails,
        it uses the speech variable, which is required.
        """
        from evennia.utils import logger, delay

        logger.log_msg("{text}".format(text=kwargs))
        # don't send any empties

        clean_kwargs = {}
        for k, v in kwargs.items():
            if v:
                clean_kwargs[k] = v
        if text:
            clean_kwargs["text"] = text

        super().msg(**clean_kwargs)
        delay(1, self.disconnect_alexa)

    @property
    def is_alexa_session(self):
        return False

    def disconnect_alexa(self):
        if self.is_alexa_session:
            for session in self.sessions.all():
                self.account.disconnect_session_from_account(session)

```

```
example rooms.py

    def return_appearance(self, looker, **kwargs):
        appearance = {'flags': [], 'name': self.get_display_name(looker), 'desc': self.db.desc or ""}

        visible = [con for con in self.contents if con != looker and con.access(looker, "view")]
        exits = [con for con in visible if con.destination]
        players = [con for con in visible if con.has_account]
        things = [con for con in visible if con not in exits and con not in players]

        appearance['exits'] = [con.get_display_name(looker) for con in exits if con.access(looker, "view")]
        appearance['players'] = [con.get_display_name(looker) for con in players if con.access(looker, "view")]
        appearance['things'] = [con.get_display_name(looker) for con in things if con.access(looker, "view")]
        appearance['card_type'] = 'traverse'

        return appearance
```
