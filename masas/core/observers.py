from flask import current_app
import smtplib


class NotifyObserver:
    def send_mail(self, subject, message):
        to = current_app.config['EMAIL_NOTIFY']
        user = current_app.config['EMAIL_USER']
        pwd = current_app.config['EMAIL_PWD']

        try:
            server = smtplib.SMTP(current_app.config['EMAIL_SERVER'])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, pwd)
            header = 'To:%s\nFrom:%s\nSubject:%s\n' % (to, user, subject)
            msg = header + '\n ' + message + '\n\n'

            server.sendmail(user, to, msg)
            server.quit()
        except(smtplib.SMTPException):
            pass

    def update(self, author):
        pass


class CreateObserver(NotifyObserver):
    def update(self, author):
        msg = 'El usuario %s ha creado un movimiento en masa. Codigo: %s' % (
               author,
               self.publisher.codigo)

        self.send_mail('Nuevo movimiento en masa', msg)


class DeleteObserver(NotifyObserver):
    def update(self, author):
        msg = 'El movimiento en masa con codigo: %s fue eliminado por %s' % (
              self.publisher.codigo,
              author)

        self.send_mail('Movimiento en masa eliminado', msg)
