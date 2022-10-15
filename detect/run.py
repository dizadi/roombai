import time

from alerter import EmailAlerter
from detector_wrapper import DetectorWrapper
from dataloader import StreamLoader

class Runner:
    def __init__(
        self,
        stream_loader,
        detector_wrapper,
        alerter,
    ):
        self._detector_wrapper = detector_wrapper
        self._stream_loader = stream_loader
        self._alerter = alerter
        self._current_detections = 0

    def run(self):
        while True:
            img, img0 = next(iter(self._stream_loader))
            detections = self._detector_wrapper.detect(img)
            num_detections = detections[0].shape[0]
            if num_detections > self._current_detections:
                save_img_path = str(time.asctime(time.localtime())) + '.jpg'
                self._detector_wrapper.save_annotated_frame(img, img0, detections, save_img_path)
                #self._detector_wrapper.show_annotated_frame(img, img0, detections)
                
                info = str(len(detections)) #+ detections[0]
                self._alerter.send_alert(
                    info,
                    save_img_path,
                )
            
            self._current_detections = num_detections


if __name__=="__main__":
    detector_wrapper = DetectorWrapper(
    )
    stream_loader = StreamLoader(
        source=0
    )
    alerter = EmailAlerter(
        distribution_list=['email@gmail.com'],
        from_email_address='email@email.com',
        from_email_name='email test',
    )

    runner = Runner(
        stream_loader=stream_loader,
        detector_wrapper=detector_wrapper,
        alerter=alerter,
    )

    runner.run()