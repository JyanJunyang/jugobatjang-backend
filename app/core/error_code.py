class ErrorCode:
    # 알 수 없는 오류
    UNKNOWN_ERROR = 1000
    # 잘못된 요청
    INVALID_REQUEST = 1001
    # 중복데이터 생성 요청
    DUPLICATED_ENTRY = 1002
    # 데이터를 찾을 수 없음
    RESOURCE_NOT_FOUND = 1003
    # 인증 실패
    UNAUTHORIZED = 1004
    # 필수 파라미터 및 RequestBody값 누락
    REQUEST_DATA_MISSING = 1005
    # 데이터 생성 불가
    DATA_CREATION_NOT_ALLOWED = 1006
    # 파일 포맷 에러
    FILE_FORMAT_ERROR = 1007
