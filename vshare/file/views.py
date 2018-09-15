from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.views import View
from user_.models import User
from django.db.models import F
import os
from file.models import File, FileType
from utils.getnow import now
from utils.page_breaker import pagebreaker
# from django.core.files.uploadedfile import InMemoryUploadedFile



# Create your views here.

class FileCenter(View):
    def get(self, request):
        # 文件展示根据get传上来的num分页显示
        depend = request.GET.get('mydepend', 'download')
        # print(depend)
        num = int(request.GET.get('num', 1))
        perpage = 20
        # 判定按时间或者下载量显示
        if depend == 'download':
            queryset = File.objects.order_by('-download').filter(is_delet=0)
            # 返回分页后的结果
            depend = 'upload_time'
            dependname = '按时间'
            page_files, range_, num_pages = pagebreaker(queryset, num, perpage)
            return render(request, 'filecenter.html', {'dependname': dependname, 'page_files': page_files, 'range_': range_, 'num_pages': num_pages, 'depend': depend})
        elif depend == 'upload_time':
            queryset = File.objects.order_by('-id').filter(is_delet=0)
            # 返回分页后的结果
            depend = 'download'
            dependname = '按下载量'
            page_files, range_, num_pages = pagebreaker(queryset, num, perpage)
            return render(request, 'filecenter.html', {'dependname': dependname, 'page_files': page_files, 'range_': range_, 'num_pages': num_pages, 'depend': depend})
        else:
            return render(request, 'Warning.html')

# 上传文件
class FileUpload(View):
    base_str = '''
    <script>
    alert("{}");
    window.location.href = "{}";
    </script>
    '''
    file_is_empty = base_str.format('你还未选择文件！', '/file/filecenter')
    file_name_repeat = base_str.format('文件名已经存在，无法上传！', '/file/filecenter')
    defeat_upload = base_str.format('上传失败，稍后再试！', '/file/filecenter')
    file_type_not_allowed = base_str.format('你选择的文件类型不被允许，详情查看页面底部提示！', '/file/filecenter')
    file_too_large = base_str.format('所选文件过大，必须小于20M！','/file/filecenter' )
    over_memory_size = base_str.format('你的内存已经用完，在个人中心删除一部分历史文件才能继续上传！', '/user_/usercenter')
    file_name_too_long = base_str.format('文件名太长已经大于100，建议你改名之后上传！', '/file/filecenter')
    imgs = [
        'jpg',
        'jpeg',
        'png',
        'bmp',
        'ico',
        'gif',
    ]
    docs = [
        'txt',
        'doc',
        'docx',
        'xls',
        'xlsx',
        'pdf',
        'md',
        'pptx',
        'ppt',
        'py',
        'json',
    ]
    # 给一个路径，获取此路径下文件大小或者文件大小
    @classmethod
    def get_size_by_path(cls, path, size=0):
        # 是一个文件则读取文件大小
        # 是一个文件夹则读取文件夹下面所有文件大小求和
        # print(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                size += os.path.getsize(os.path.join(root, file))
            for dir in dirs:
                new_path = os.path.join(root, dir)
                return cls.get_size_by_path(new_path, size)
        return size
    # 文件名太长判断
    @staticmethod
    def _is_file_name_too_long(file_name):
        from vshare.settings import FILE_NAME_MAX_SIZE
        if len(file_name) > FILE_NAME_MAX_SIZE:
            return True
        return False
    # 判断文件类型
    @staticmethod
    def file_type(file_name):
        end_ = file_name.split('.')[-1]
        if end_ in FileUpload.imgs:
            return 'imgs'
        elif end_ in FileUpload.docs:
            return 'docs'
        else:
            return 'unknow'
    # 获取user
    @staticmethod
    def get_user_info_by_id(user_id):
        user = User.objects.get(id=user_id)
        # print(user)
        return user
    # 为用户准备文件存放位置
    @staticmethod
    def init_dir_for_user_file(user):
        from vshare.settings import BASE_FILE_DIR
        user_dir = os.path.join(BASE_FILE_DIR, user.account)
        user_imgs_dir = os.path.join(user_dir, 'imgs')
        user_docs_dir = os.path.join(user_dir, 'docs')
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        if not os.path.exists(user_imgs_dir):
            os.mkdir(user_imgs_dir)
        if not os.path.exists(user_docs_dir):
            os.mkdir(user_docs_dir)
        return (user_dir, user_imgs_dir, user_docs_dir)
    # 传入文件对象，文件类型，和用户对象，写文件
    @staticmethod
    def save_file(file, type_, imgs_dir, docs_dir):
        if type_ == 'imgs':
            filepath = os.path.join(imgs_dir, file.name)
        else:
            filepath = os.path.join(docs_dir, file.name)
        with open(filepath, 'wb') as fb:
            # 文件分片读取,每次2048字节，以免占用太多内存
            from vshare.settings import UP_FILE_CHUNK_SIZE
            for chunk in file.chunks(UP_FILE_CHUNK_SIZE):
                fb.write(chunk)
        return filepath
    # 判断用户内存是否已经用完，每人500M
    def _is_over_memory_size(self, user_dir, file):
        used_size = self.get_size_by_path(user_dir)
        # print(used_size)
        from vshare.settings import ALL_MAX_SIZE, VIP_ALL_MAX_SIZE, VIP_USER_LIST
        # print(user_dir.split('\\')[-1])
        if user_dir.split('\\')[-1] in VIP_USER_LIST:
            SIZE = VIP_ALL_MAX_SIZE
        else:
            SIZE = ALL_MAX_SIZE
        if int(used_size)+int(file.size) > SIZE:
            return True
        else:
            return False
    # 判断文件大小
    @staticmethod
    def _is_file_too_large(file, user_account):
        file_size = int(file.size)
        # print(file_size, '--------')
        # 一次上传必须小于20M
        from vshare.settings import SIGNAL_MAX_SIZE, VIP_SIGNAL_MAX_SIZE, VIP_USER_LIST
        if user_account in VIP_USER_LIST:
            SIZE = VIP_SIGNAL_MAX_SIZE
        else:
            SIZE = SIGNAL_MAX_SIZE
        if file_size > SIZE:
            return True
        else:
            return False

    def get(self, request):
        return render(request, 'Warning.html')

    def post(self, request):
        user_id = request.POST.get('user_id')
        file = request.FILES.get('upfile')
        # 文件内容判空
        if not file:
            return HttpResponse(FileUpload.file_is_empty)
        # 文件名长短判断
        if self._is_file_name_too_long(file.name):
            return HttpResponse(FileUpload.file_name_too_long)
        # 文件类型判断
        type_ = self.file_type(file.name)
        if type_ == 'unknow':
            return HttpResponse(FileUpload.file_type_not_allowed)
        else:
            type_id = FileType.objects.get(filetype=type_).id
            # print(type_id)
        # 准备存放位置
        user = self.get_user_info_by_id(user_id)
        user_dir, imgs_dir, docs_dir = self.init_dir_for_user_file(user)
        # 判断单个文件大小是否超标
        if self._is_file_too_large(file, user.account):
            return HttpResponse(FileUpload.file_too_large)
        # 判断用户内存是否用完
        if self._is_over_memory_size(user_dir, file):
            return HttpResponse(FileUpload.over_memory_size)
        # 写文件
        try:
            filepath = self.save_file(file, type_, imgs_dir, docs_dir)
        except:
            return HttpResponse(FileUpload.defeat_upload)
        # 数据库更新, 倘若数据库出错，则删除刚才的文件
        upload_time = now()
        content_type = file.content_type
        if File.objects.filter(name=file.name).count()>0:
            return HttpResponse(FileUpload.file_name_repeat)
        try:
            File.objects.create(
                name=file.name,
                path=filepath,
                upload_time=upload_time,
                download=0,
                content_type=content_type,
                is_delet=0,
                filetype_id=type_id,
                user_id=user.id
            )
        except:
            os.remove(filepath)
            return HttpResponse(FileUpload.defeat_upload)
        else:
            # 返回
            return HttpResponseRedirect('/file/filecenter')

# 下载文件
class FileDownload(View):
    from vshare.settings import DOWN_FILE_CHUNK_SIZE
    # 文件迭代器，用于文件下载分片处理
    @staticmethod
    def file_iterator(path, chunk_size=DOWN_FILE_CHUNK_SIZE):
        with open(path, 'rb') as fr:
            while True:
                chunk = fr.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break
        # 删除服务器上的压缩包
        os.remove(path)

    def get(self, request):
        # 获取文件id
        file_id = request.GET.get('f_id', None)
        if not file_id:
            return render(request, 'Warning.html')
        # 获取文件存储路径
        try:
            file = File.objects.get(id=file_id)
        except:
            return HttpResponse('服务器维修中，稍后再试！')
        # 文件下载------------
        from vshare.settings import BASE_FILE_DIR, LOGO_FILE_NAME
        logo_path = os.path.join(BASE_FILE_DIR, LOGO_FILE_NAME)
        zip_path = self.make_zip(file.path, logo_path, file.name, LOGO_FILE_NAME)
        response = StreamingHttpResponse(self.file_iterator(zip_path))
        response['Content-Type'] = 'application/zip'
        # 设置文件下载格式和名字
        # print(file.name.split('.')[0])
        response['Content-Disposition'] = 'attachment;filename="{}.zip"'.format(file.name.split('.')[0])
        # 更新数据库下载次数
        try:
            File.objects.filter(id=file.id).update(download=F('download')+1)
        except:
            pass
        return response

    def post(self, request):
        return render(request, 'Warning.html')

    # 自动将logo和目标打包成zip, 返回zip路径
    def make_zip(self, file_path, logo_path, file_name, logo_name):
        import zipfile, shutil
        from vshare.settings import BASE_FILE_DIR
        zip_dir = os.path.join(BASE_FILE_DIR, 'vshare_tmp_zip_file')
        if not os.path.exists(zip_dir):
            os.mkdir(zip_dir)
        file_copy = os.path.join(zip_dir, file_name)
        logo_copy = os.path.join(zip_dir, logo_name)
        shutil.copyfile(file_path, file_copy)
        shutil.copyfile(logo_path, logo_copy)
        ziped_file_path = os.path.join(BASE_FILE_DIR, file_name)
        # 删除zips里面的临时文件
        shutil.make_archive(ziped_file_path, 'zip', zip_dir)
        os.remove(file_copy)
        os.remove(logo_copy)
        ziped_file_name = '{}.zip'.format(ziped_file_path)
        return ziped_file_name










