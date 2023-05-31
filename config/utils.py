# for django-taggit
def custom_tag_string(tag_string):
    '''
    입력값을 스페이스로만 구분해 태그로 저장합니다.
    '''
    if not tag_string:
        return []
    return tag_string.split(' ')