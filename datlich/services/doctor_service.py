from ..models import Doctor

def create_new_doctor(user):
    # Khởi tạo một đối tượng Doctor mới cho người dùng
    Doctor.objects.create(
        user=user,
        position='Default Position',  # Có thể thay đổi tùy theo thông tin nhập vào
        description='Default Description',  # Mô tả mặc định hoặc tùy chỉnh
        room_address='Room 101',  # Địa chỉ phòng mặc định hoặc tùy chỉnh
        service_prices=100000  # Giá dịch vụ mặc định hoặc tùy chỉnh
    )
