import emails
import time


class EmailAlerter:
    def __init__(
        self,
        distribution_list,
        from_email_address,
        from_email_name,
        alert_image_name='alert.jpg',
        alert_message_subject='Security Alert'
    ):
        self._distribution_list = distribution_list
        self._from_email_address = from_email_address
        self._from_email_name = from_email_name
        self._alert_image_name = alert_image_name
        self._alert_message_subject = alert_message_subject

    def send_alert(
        self,
        info,
        image_path,
    ):
        message = self.build_email(info, image_path)
        try:
            self.send_email(message)
        except:
            print("Failed to send alert")

    def build_email(
        self,
        info,
        attachments,
    ):
        local_time_obj = time.localtime()
        time_string = time.asctime(local_time_obj)
        alert_string_html = f"<p>ALERT<br>A {info} was detected on camera {time_string}"
        message = emails.html(html=alert_string_html,
                            subject=self._alert_message_subject,
                            mail_from=(self._from_email_name, self._from_email_address))
        message.attach(data=open(attachments, 'rb'), filename=self._alert_image_name)

        return message

    def send_email(
        self,
        message,
    ):
        for person in self._distribution_list:
            r = message.send(to=person, smtp={'host': 'localhost', 'timeout': 5})
            assert r.status_code == 250, f'Failed to send email to {person}'


if __name__=="__main__":
    alerter = EmailAlerter([''], "security@house.test", "TEST")
    alerter.send_alert(
        "Testing 123",
        "",
        ""
    )
