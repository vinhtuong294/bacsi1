from ..models import Patient

def create_new_patient(user):
    # Khởi tạo một đối tượng Patient mới cho người dùng
    Patient.objects.create(
        name=user.fullname,
        user=user,
        nhommau='O',  # Giá trị mặc định hoặc tùy chỉnh dựa trên yêu cầu của ứng dụng
        cannang=0.0,  # Giá trị mặc định hoặc tùy chỉnh
        chieucao=0.0,  # Giá trị mặc định hoặc tùy chỉnh
        benhnen='N/A'  # Giá trị mặc định hoặc tùy chỉnh
    )
