from django.core.exceptions import ValidationError
import os
    


def validate_file_size(value):
    filesize= value.size
    if filesize > 10485760: #size in byte
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def file_size_photo(value): # add this to some file where you can import it from
    limit = 0.15 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 150KB.')



def file_size_profile_photo(value): # add this to some file where you can import it from
    limit = 0.06 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 60KB.')        



def file_size_pdf(value): # add this to some file where you can import it from
    limit = 0.25 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 250KB.') 



def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')       
