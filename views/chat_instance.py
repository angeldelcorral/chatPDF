from common.common_functions import ChatPDFBot, ReturnJsonRequest


def get_answer(data_dict):
    chat_instance = ChatPDFBot()
    question = data_dict.get('message')
    # if question is None:
    #     question = request.json.get('message') . 
    chat_instance.chat_pdf_bot(question)
    result = {
        'message': chat_instance.answers,
        'user_id': '1',
        'user_name': 'PDF Bot'
    }


    return_format = ReturnJsonRequest()
    
    return return_format.json_return_format(200, "Encontre la respuesta.", result)    