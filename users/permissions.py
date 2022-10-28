from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadonly(BasePermission):
    # 인증된 유저에 한해, 목록조회/포스팅등록을 허용
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)  # 인증이 되야만 허용

    # 작성자에 한해, Record에 대한 수정/삭제 허용
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # PUT, DELETE 요청에 대해, 작성자일 경우에만 요청 허용
        return obj.user_id == request.user.user_id


class IsUserOrWriteo(BasePermission):
    def has_permission(self, request, view):
        # 읽기는 staff만 허용
        if request.method == "GET":
            return request.user.is_staff
        return True
