import io

from starlite import State, Partial, post, Request, patch
from starlite.controller import Controller

from ..models import RequestQrCode, ResponseQrCode, Qr, RequestQrUrlUpdate, ResponseQrUrlUpdate
from ...core.library import try_shorten_url


class QrCodeController(Controller):
    path = "/qr"

    @post("/")
    async def post_qr_image(self,
                            state: State,
                            request: Request,
                            data: Partial[RequestQrCode],
                            ) -> ResponseQrCode:
        converted_to_url_response = try_shorten_url(data.msg, state=state, request=request)
        output_url = converted_to_url_response['shorturl'] if converted_to_url_response is not None else data.msg

        qr = Qr(msg=output_url, size=data.size, options=data.options, background_image_url=data.background_url)

        img_bytes = io.BytesIO()
        qr.img.save(img_bytes, format=qr.format)
        img_bytes.seek(0)
        qr_image_url = state.linx.upload(img_bytes, randomize_filename=True, expiration_seconds=60)

        res = ResponseQrCode(
            msg=data.msg,
            options=data.options,
            image_url=qr_image_url.json()['direct_url'],
            update_token=converted_to_url_response['url']['update_token']
        )
        if converted_to_url_response is not None:
            res.original_msg = data.msg
            res.msg = output_url

        return res

    @patch("/url")
    async def update_url(self,
                         state: State,
                         request: Request,
                         data: Partial[RequestQrUrlUpdate]
                         ) -> ResponseQrUrlUpdate:
        result = state.yourls.token_update_url(shorturl=data.shorturl, token=data.token,
                                               new_url=data.new_url, new_title=data.new_title)
        res = ResponseQrUrlUpdate(success=result)
        return res
