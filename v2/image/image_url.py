# 킹콩의 이미지 생성 중...
# https://oaidalleapiprodscus.blob.core.windows.net/private/org-2g89ZDcaFj99ZvEkVjKHjQ07/user-aqKfjdrelqsWLJfdG6RAEFsP/img-TOY0rpWsUxDyE4Lso3364C8T.png?st=2025-03-06T06%3A09%3A49Z&se=2025-03-06T08%3A09%3A49Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-06T03%3A56%3A51Z&ske=2025-03-07T03%3A56%3A51Z&sks=b&skv=2024-08-04&sig=1dav580gDvTG0ylRl/BmkwgD1mMP%2BHVMU3JYeCsRMO8%3D
# 다미의 이미지 생성 중...
# https://oaidalleapiprodscus.blob.core.windows.net/private/org-2g89ZDcaFj99ZvEkVjKHjQ07/user-aqKfjdrelqsWLJfdG6RAEFsP/img-tAcZCGaEIAcYIDYL4m28YIy8.png?st=2025-03-06T06%3A10%3A09Z&se=2025-03-06T08%3A10%3A09Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-06T02%3A19%3A40Z&ske=2025-03-07T02%3A19%3A40Z&sks=b&skv=2024-08-04&sig=epq1aC6oLqyl8w7bS9znt0Vtjp91Y1rZDKJezCkPIoA%3D
# 큐티예나의 이미지 생성 중...
# https://oaidalleapiprodscus.blob.core.windows.net/private/org-2g89ZDcaFj99ZvEkVjKHjQ07/user-aqKfjdrelqsWLJfdG6RAEFsP/img-pbUeipYUdyhfo0BPjVuLBlJ1.png?st=2025-03-06T06%3A10%3A35Z&se=2025-03-06T08%3A10%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-06T03%3A10%3A19Z&ske=2025-03-07T03%3A10%3A19Z&sks=b&skv=2024-08-04&sig=yoXMSfVdRA6lRUx6N3WYQpzhYxCI8KnHHeygUEbYidY%3D
# 흑진의 이미지 생성 중...
# https://oaidalleapiprodscus.blob.core.windows.net/private/org-2g89ZDcaFj99ZvEkVjKHjQ07/user-aqKfjdrelqsWLJfdG6RAEFsP/img-ZzYcUib9IbEh2juPLYzbVfq4.png?st=2025-03-06T06%3A11%3A04Z&se=2025-03-06T08%3A11%3A04Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-06T02%3A48%3A20Z&ske=2025-03-07T02%3A48%3A20Z&sks=b&skv=2024-08-04&sig=yxCSe7wjX/zjTwGvjK3h1SrEt3P33ougo9zkLXtYF/w%3D
# 보이드 레조넌스의 이미지 생성 중...
# https://oaidalleapiprodscus.blob.core.windows.net/private/org-2g89ZDcaFj99ZvEkVjKHjQ07/user-aqKfjdrelqsWLJfdG6RAEFsP/img-KqO8TNmx6H6zGPAdSyn1Oo4f.png?st=2025-03-06T06%3A11%3A29Z&se=2025-03-06T08%3A11%3A29Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-03-06T03%3A01%3A57Z&ske=2025-03-07T03%3A01%3A57Z&sks=b&skv=2024-08-04&sig=K%2B0XIi7/ucuEB8AvODNy1egDa6H6BfsZJZ0xagj%2BTG8%3D

from enum import Enum


class ImageURL(Enum):
    KING_KONG = "https://raw.githubusercontent.com/hyukjunkim1116/scoop-ai-discord/main/v2/image/image_files/kingkong.png"
    DAMI = "https://raw.githubusercontent.com/hyukjunkim1116/scoop-ai-discord/main/v2/image/image_files/dami.png"
    CUTIE_YENA = "https://raw.githubusercontent.com/hyukjunkim1116/scoop-ai-discord/main/v2/image/image_files/yena.png"
    HEUKJIN = "https://raw.githubusercontent.com/hyukjunkim1116/scoop-ai-discord/main/v2/image/image_files/heukjin.png"
    VOID_RESONANCE = "https://raw.githubusercontent.com/hyukjunkim1116/scoop-ai-discord/main/v2/image/image_files/resonance.png"
    CHARACTER_MAP = {
        "킹콩": KING_KONG,
        "다미": DAMI,
        "큐티예나": CUTIE_YENA,
        "흑진": HEUKJIN,
        "보이드 레조넌스": VOID_RESONANCE
    }





