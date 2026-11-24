"""Module tinh chỉnh và sửa triệt để các khối lệch dòng cho Triệu Châu Ngữ Lục (CV09).

Xử lý dứt điểm:
1. Xóa câu tiếng Anh thừa ở Tắc 378 (The master said, “Good Heavens!”).
2. Đồng nhất thứ tự Tắc 475 và 476: Đưa Văn Viễn luận nghĩa lên trước Trụ đá khắc kinh theo đúng nguyên tác Hán CBETA Q14.
3. Chuẩn hóa ranh giới và vai đối thoại cho tất cả các khối công án bị lệch dây chuyền:
   - 157-158 (Tắc 276-277)
   - 305-311 (Tắc 331-334: Cầu đá & Tô châu)
   - 333-334 (Tắc 339)
   - 470-473 (Tắc 384)
   - 582-586 (Tắc 419-420)
   - 630-631 (Tắc 437-439)
   - 635-641 (Tắc 440-441)
   - 648-672 (Tắc 442-449)
   - 708-729 (Tắc 453-458)
   - 736-738 (Tắc 459-460)
   - 748-757 (Tắc 463-465)
   - 788-807 (Tắc 469-473)
   - 810-843 (Tắc 474-484)
   - 854-863 (Tắc 487-491)
   - 887-900 (Tắc 496-499)
   - 931-956 (Tắc 507-517)
   - 972-cuối (Tắc 525: Khúc ca 12 giờ, Tắc 521-524, Triệu Vương tán, Khóc Triệu Châu)
4. Khôi phục câu mở đầu bị cắt mất tại Tắc 473 (Sư hỏi trị nhật ăn rau sống hay rau chín).
5. Xóa triệt để 4 vị trí lặp dòng / lặp vế (716-718, 772, 958, 983).
6. Căn chỉnh chuẩn xác 100% 11 điểm lệch ranh giới đối thoại ngắn (67-68, 357-360, 694-698, 703-704, 711-713, 715-716, 778-780, 932-933, 947-948, 952-953, 954-956).
"""

from typing import List, Tuple


def apply_precise_fixes(pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Căn chỉnh chi tiết 16 điểm theo phản hồi rà soát toàn diện."""
    p = [list(pair) for pair in pairs]

    # Thực hiện từ cuối lên đầu để các chỉ số phía trước không bị xê dịch

    # 1. Điểm 5: Dòng 983 (Tắc 517) - Xóa vế lặp 'Thủ tọa không đáp được.' ở đầu cột VI
    p[982] = [p[982][0], "Có vị tú tài gặp Sư bèn khen ngợi:  - Hòa thượng là cổ Phật."]

    # 2. Điểm 16 & Điểm 4: Dòng 954-959 (Tắc 506-507) - Căn chỉnh ranh giới cầu đá & viện Tân La, xóa câu lặp 'cách biển'
    block_506_507 = [
        ("師與首座看石橋，乃問首座：是什麼人造？ 云：李膺造。", "Sư cùng thủ tọa xem cầu đá. Sư hỏi Thủ tọa:   - Người nào tạo chiếc cầu? Thủ tọa đáp:  - Lý Ưng tạo."),
        ("師云：造時向什麼處下手？", "- Lúc tạo nhằm vào đâu để tay?"),
        ("座無對，師云：尋常說石橋問，著下手處也不知。", "Thủ tọa không đáp được. Sư bảo:  - Bình thường nói cầu đá, hỏi đến chỗ để tay cũng chẳng biết."),
        ("有新羅院主請師齋，師到門首問：此是什麼院？", "Có viện chủ Tân La thỉnh Sư thọ trai, Sư đến trước cổng hỏi: “Ðây là chùa  nào?”"),
        ("云：新羅院。", "Viện chủ thưa: “Viện Tân La”."),
        ("師云：我與你隔海。", "Sư bảo: “Ta cùng ông cách biển”.")
    ]
    p[953:959] = [list(x) for x in block_506_507]

    # 3. Điểm 15: Dòng 952-953 (Tắc 505) - Trả 'Tăng phất tay áo ra đi.' về đúng dòng 953
    p[951] = ["師云：孫臏門下因 什麼鑽龜？", "Sư bảo:  - Dưới cửa Tôn Tẩn nhân gì dùi rùa?"]
    p[952] = ["僧拂袖出去，師云：將為當榮，折他雙足。", "Tăng phất tay áo ra đi. Sư bảo:  - Tuy sắp được vinh hiển mà hai chân bị chặt ."]

    # 4. Điểm 14: Dòng 947-948 (Tắc 504) - Trả 'Tăng xòe tay.' về đúng dòng 948
    p[946] = ["師云：還見文殊也無？", "- Có thấy Văn-thù hay không?"]
    p[947] = ["僧展手，師云：展手頗 多，文殊難覩。", "Tăng xòe tay. Sư bảo:  - Ông có thể xòe tay nhiều lần, nhưng ai thấy được Văn-thù?"]

    # 5. Điểm 13: Dòng 932-933 (Tắc 499-500) - Tách 'Sư đến Bá Trượng.' sang đầu dòng 933
    p[931] = ["師放下掃 呵呵大笑而去，大慈便歸方丈。", "Sư buông chổi xuống, cười to ha hả mà đi. Ðại Từ trở về phương trượng."]
    p[932] = ["師到百丈，百丈問：從 什麼處來？", "Sư đến Bá Trượng. Bá Trượng hỏi:  - Từ đâu đến đây?"]

    # 6. Điểm 1: Dòng 826 (Tắc 473) - Khôi phục câu mở đầu bị cắt mất
    block_473 = [
        ("師問菜頭：今日喫生菜？ 熟菜？", "Sư hỏi trị nhật:  - Hôm nay ăn rau sống hay rau chín?"),
        ("菜頭提起一莖菜。", "Trị nhật đưa lên một cọng rau.")
    ]
    p[825:826] = [list(x) for x in block_473]

    # 7. Điểm 3 & Điểm 12: Dòng 771-781 (Tắc 465) - Xóa lặp '云：不會。' ở dòng 772, khớp chuẩn 3 dòng 778-780
    block_465 = [
        ("云：不會。", "Tăng thưa: “Chẳng lãnh hội”."),
        ("師却云：此去舒州有投子山和尚，你去禮拜，問取因緣。 相契不用更來，不相契却來。", "Sư lại bảo: “Từ đây hãy đi đến Châu Thư có hòa thượng ở núi Ðầu Tử, ông  hãy đến đó lễ bái và hỏi. Nhân duyên khế hợp thì chẳng cần trở lại, chẳng khế  hợp thì trở lại đây”."),
        ("其僧便去。", "Vị tăng ấy liền đi."),
        ("纔到投子和尚處，投子乃問：近離 什麼處？", "Vừa đến chỗ hòa thượng Ðầu Tử, Ðầu Tử hỏi: “Vừa rời chỗ  nào đến?”"),
        ("云：離趙州特來禮拜和尚。", "Tăng thưa: “Rời Triệu Châu đến đây lễ bái hòa thượng”."),
        ("投子云：趙州老人 有何言句？", "Ðầu Tử bảo: “Ông già Triệu Châu có lời gì chỉ dạy?”"),
        ("僧乃具舉前話。", "Tăng bèn thuật lại lời trước."),
        ("投子乃下禪床行三五步 却坐云：會麼？", "Ðầu Tử bước xuống giường thiền, đi năm ba bước, rồi ngồi lại bảo: “Lãnh hội  chăng?”"),
        ("僧云：不會。", "Tăng thưa: “Chẳng lãnh hội”."),
        ("投子云：你歸舉似趙州。", "Ðầu Tử bảo: “Ông về đi thuật lại cho Triệu Châu”."),
        ("其僧却歸舉似師，", "Vị tăng ấy trở về thuật lại cho Sư."),
        ("師云：還會麼？ 云：未會。", "Sư bảo:   - Lãnh hội chăng? Tăng thưa:   - Chưa lãnh hội."),
        ("師云：也不較多也。", "Sư bảo:   - Cũng chẳng sai khác.")
    ]
    p[770:781] = [list(x) for x in block_465]

    # 8. Điểm 10, Điểm 11 & Điểm 2: Dòng 711-721 (Tắc 452-453) - Xóa lặp '披衲衣來否', căn chuẩn ranh giới 1-1
    block_452_453 = [
        ("云： 既不在心數裏，和尚為什麼覓？", "- Ðã chẳng ở trong tâm sở, hòa thượng vì cái gì tìm?"),
        ("師云：為你道不得。", "- Vì ông nói không được."),
        ("云： 法過眼、耳、鼻、舌、身、意而不解，作麼生道不得？", "- Pháp vượt trên mắt tai mũi lưỡi thân ý, nhưng chẳng thể nhận biết. Vậy làm  sao có thể nói được?"),
        ("師云：喫 我涕唾。", "- Ăn đàm dãi của ta."),
        ("師問僧：你曾看法華經麼？ 云：曾看。", "Sư hỏi vị tăng: “Ông từng xem kinh Pháp Hoa chăng?” Tăng thưa: “Dạ từng xem”."),
        ("師云：經中 道：衲衣在空閑，假名阿練若，誑惑世間人。", "Sư bảo:  - Trong kinh nói ‘Khoác nạp y và ở nơi vắng vẻ, được gọi là A-luyện-nhã,  người thế gian bị dối gạt vì điều đó’."),
        ("你作麼生 會？", "Ông làm sao lãnh hội?"),
        ("僧擬禮拜，", "Tăng lễ bái."),
        ("師云：你披衲衣來否？", "Sư bảo: - Ông có khoác nạp y chăng?"),
        ("云：披來。", "- Có khoác."),
        ("師云：莫惑我。", "- Chớ lừa ta."),
        ("云：如何得不惑去？", "- Làm sao để chẳng lừa thầy?"),
        ("師云：自作活計，莫取老僧語。", "- Ta tự tạo kế sống, chớ nhận đùa lời của lão tăng.")
    ]
    p[710:721] = [list(x) for x in block_452_453]

    # 9. Điểm 8 & Điểm 9: Dòng 694-704 (Tắc 450-452) - Tách bạch '主無語' <-> 'Tọa chủ im lặng', '主無對' <-> 'Tọa chủ không đáp được'
    block_450_452 = [
        ("師云：直饒你問得答得，總屬經論佛法未在。", "- Dù cho ông hỏi được và đáp được, thảy đều thuộc kinh luận, chẳng phải Phật  pháp."),
        ("主無語。", "Tọa chủ im lặng không đáp."),
        ("師問一行者：從什麼處來？", "Sư hỏi một cư sĩ tập tu:  - Từ đâu đến đây?"),
        ("云：北院來。", "Cư sĩ đáp:   - Từ một viện ở phía bắc đến."),
        ("師云：那 院何似者院？", "- Sao viện đó giống viện này?"),
        ("行者無對。", "Cư sĩ không đáp được."),
        ("有僧在邊立，師令代行者語， 僧代云：從那院來。", "Có vị tăng đứng bên cạnh, Sư sai tăng đáp thay cư sĩ. Tăng nói:  - Từ viện kia đến."),
        ("師笑之。", "Sư cười."),
        ("師又令文遠代之，文遠云： 行者還是不取師語話。", "Sư lại sai Văn Viễn đáp thay. Văn Viễn nói:  - Con chưa có lời nào với Thầy."),
        ("師問座主：所習何業？", "Sư hỏi tọa chủ:  - Ðã quen sự nghiệp (tu pháp môn) gì?"),
        ("云：講維 摩經。", "Tọa chủ thưa:  - Giảng Kinh Duy-ma."),
        ("師云：維摩經步步是道場，座主在什麼處？", "Sư bảo:  - Kinh Duy-ma nói ‘Đạo tràng ở mỗi bước chân‘. Tọa chủ ở chỗ nào?"),
        ("主無 對。", "Tọa chủ không đáp được."),
        ("師令全益代座主語，全益云：只者一問，可識道場 麼？", "Sư sai Toàn Ích (một đệ tử của Sư) đáp thay tọa chủ. Toàn Ích nói:  - Chỉ một câu hỏi này mà có thể nhận biết đạo tràng chăng?")
    ]
    p[693:704] = [list(x) for x in block_450_452]

    # 10. Điểm 7: Dòng 357-360 (Tắc 344) - Căn chỉnh ranh giới 4 dòng hạt châu của học nhân
    p[356] = ["師云：高聲問。", "Sư bảo: “Hỏi to lên!”"]
    p[357] = ["僧禮拜，師 云：不解問。 何不道：高下即不問，如何是學人珠？ 何不與麼問？", "Tăng lễ bái. Sư bảo:   - Ông chẳng biết hỏi. Sao chẳng nói ‘Có tiếng hay lặng thinh thì chẳng hỏi, thế  nào là hạt châu của học nhân?’ Sao ông chẳng hỏi như thế?"]
    p[358] = ["僧便再問，", "Vị tăng liền hỏi lại câu trên."]
    p[359] = ["師云：洎合放過者漢。", "Sư bảo:   - Ta cũng muốn cho qua gã này."]

    # 11. Điểm 6: Dòng 67-68 (Tắc 242) - Đưa '師應諾。' xuống đúng câu đáp
    p[66] = ["問：如何是一句？", "Tăng hỏi: “Thế nào là một câu?”"]
    p[67] = ["師應諾。 僧再 問，師云：我不患聾。", "Sư ứng thinh: “Dạ!” Tăng hỏi lại câu trên, Sư bảo: “Ta chẳng bệnh điếc”."]

    return [(h, v) for h, v in p]


def refine_trieu_chau_pairs(orig_pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Thay thế các khối bị lệch dòng bằng các cặp đã được căn chỉnh chuẩn xác 100%."""

    block_1 = [
        ("問：道人相見時如何？ 師云：呈漆器。", "Tăng hỏi: “Khi đạo nhân gặp nhau thì thế nào?” Sư đáp: “Trình thùng sơn.”"),
        ("問：諦為什麼觀不得？", "Tăng hỏi: “Chân lý (đế), vì sao quán chẳng được?”")
    ]

    block_2_3 = [
        ("問：久嚮趙州石橋，到來只見掠彴子。", "Tăng hỏi: “Từ lâu nghe tiếng cầu đá của Triệu Châu, đến đây chỉ thấy cầu khỉ”."),
        ("師云：闍黎只見掠彴子，不見趙州石橋。", "Sư bảo: “Xà-lê chỉ thấy cây cầu khỉ [nên] chẳng thấy cầu đá Triệu Châu”."),
        ("云：如何是石橋？", "- Thế nào là cầu đá?"),
        ("師云：過來，過來。 又云：度驢度馬。", "Sư bảo: - Đi qua! Đi qua! Lại bảo: - Lừa qua, ngựa qua."),
        ("問：和尚姓什麼？", "Tăng hỏi: “Hòa thượng họ gì?”"),
        ("師云：常州有。", "Sư đáp: “Thường châu”."),
        ("云：甲子多少？", "- Bao nhiêu tuổi?"),
        ("師云：蘇州有。", "- Tô châu."),
        ("上堂。 云：纔有是非，紛然失心，還有答話分也無？", "Sư thượng đường bảo: “‘Vừa có phải quấy thì lăng xăng mất tâm’. Có ai đáp thoại hay không?”")
    ]

    block_4 = [
        ("師云：我不將境示人。", "Sư đáp: “Ta chẳng đem cảnh chỉ dạy ông."),
        ("若將境示闍黎，即埋沒闍黎去也。", "Nếu ta đem cảnh chỉ dạy xà-lê, liền chôn vùi xà-lê mất”."),
        ("云：爭奈者箇何？ 師便珍重。", "Sư nói tiếp: “Ông làm sao với cái này?” Rồi chào lui.")
    ]

    block_5 = [
        ("問：三處不通，如何離識？", "Tăng hỏi:  - Ba chỗ chẳng thông, thế nào lìa thức?"),
        ("師云：識是分外。", "Sư đáp:  - Thức qua khỏi tầm với của ông.")
    ]

    block_6 = [
        ("師云：人從陳州來，不得許州信。", "Sư đáp:  - Người từ châu Trấn đến, ông chẳng được tin tức của châu Hứa."),
        ("問：開口是有為，如何是無為？", "Tăng hỏi:  - Mở miệng là hữu vi, thế nào là vô vi?"),
        ("師以手示之云：者箇是無為。", "Sư chỉ vào tay, bảo:  - Đây là vô vi."),
        ("云：者箇是有為，如何是無為？", "- Đó là hữu vi, thế nào là vô vi?"),
        ("師云：無為。", "- Vô vi."),
        ("云：者箇是有為？", "- Đó là hữu vi?"),
        ("師云：是有為。", "- Là hữu vi.")
    ]

    block_7 = [
        ("師云：會得祖意，便會教意。", "Sư đáp:  - Nếu ông lãnh hội được ý của tổ liền lãnh hội ý của giáo."),
        ("問：如何是異類中行？ 師云：唵啉唵", "Tăng hỏi:  - Thế nào là đi trong dị loại (Cái dụng của sai biệt trong tính bình đẳng)? Sư đáp:  - Án-bộ-lâm, án-bộ-lâm."),
        ("問：高峻難上時如何？", "Tăng hỏi: “Khi cao vót khó lên thì thế nào?”"),
        ("師云：老僧自住峯頂。", "Sư đáp: “Lão tăng tự đang ở chót đảnh”."),
        ("云：爭奈曹溪路側何？ 師云：曹溪是惡。", "- Làm thế nào ứng phó khi đường Tào Khê dốc đứng? - Tào Khê không phải đường tốt."),
        ("云：今時為什麼不到？ 師云：是渠高峻。", "- Gần đây vì sao chẳng có ai đến được? - Vì đường cao vót.")
    ]

    block_8 = [
        ("問：朗月當空時如何？", "Tăng hỏi:   - Khi trăng sáng giữa trời thì thế nào?"),
        ("師云：猶是堦下漢。 云：請師接上堦。", "Sư đáp:   - Ông vẫn là kẻ ở thềm bậc. - Thỉnh thầy tiếp cho con qua khỏi thềm bậc."),
        ("師云：月落了，來相見。", "- Khi trăng đã xuất hiện, hãy đến gặp ta."),
        ("師有時示眾云：老僧初到藥山時得一句子，直至如今", "Có lúc Sư dạy chúng: “Lão tăng lúc mới đến Dược Sơn được một câu,  từ đó đến nay được no tràn”."),
        ("大王禮拜了，左右問：土王來為什麼不起？", "ÐỐI  CƠ  KHÁM  BIỆN  Nhân Sư đang ngồi thiền trong thất, chủ sự báo vua đến viếng thăm. Xong, kẻ thân cận hỏi:  - Vua đến, vì sao chẳng đứng dậy?"),
        ("師云：你不 會老僧者裏下等人來，出三門接；中等人來，下禪床 接；上等人來，禪床上接。", "Sư bảo:  - Ông chẳng hiểu. Lão tăng ở đây người bậc hạ đến thì ra cổng tiếp, người bậc  trung đến thì xuống giường tiếp, người bậc thượng đến thì ở trên giường tiếp."),
        ("不可喚大王作中等．下等人 也，恐屈大王。", "Ta  chẳng thể gọi vua là người bậc trung hay bậc hạ, e hạ thấp vua."),
        ("大王歡喜，再三請入內供養。", "Vua vui vẻ khi nghe lời ấy, ân cần mời vào cung ba lần cúng dường.")
    ]

    block_9 = [
        ("師因問周員外：你還夢見臨濟也無？", "Nhân Sư hỏi viên ngoại họ Chu:  - Ngài có mộng thấy Lâm Tế hay không?"),
        ("員外竪起拳，師云：那邊見？", "Viên ngoại giơ nắm tay lên. Sư bảo:  - Thấy bên nào?"),
        ("外云：者邊見。", "- Thấy bên này."),
        ("師云：什麼處見臨濟？", "- Chỗ nào thấy Lâm Tế?"),
        ("員外無對。", "Viên ngoại không đáp được."),
        ("師問周員外：什麼處來？", "Sư hỏi viên ngoại:  - Ở đâu đến?"),
        ("云：非來非去。", "Viên ngoại thưa:  - Chưa từng đến, chưa từng đi."),
        ("師云：不是老鵶飛來飛去。", "- Dù chẳng phải con quạ già, nó bay đến rồi bay đi."),
        ("師示眾云：纔有是非，紛然失心，還有答話分也無？", "Sư dạy chúng:  - ‘Vừa có phải quấy, lăng xăng mất tâm’. Các ông có đáp thoại hay không?"),
        ("後有僧舉似洛浦，洛浦扣齒；又舉似雲居，雲居云：何必？", "Sau, có vị tăng thuật lại cho Lạc Phố, Lạc Phố gõ răng [để trả lời]. Lại thuật lại cho Vân Cư, Vân Cư bảo: “Có cái gì cần trả lời ở đây?”")
    ]

    block_10 = [
        ("師云：我自理經也不得。", "Sư bảo: “Ta không thể tự sắp xếp lại lời kinh được”."),
        ("因僧辭去，師云：闍黎出外，忽有人問：還見趙州否？ 你作麼生祇對？", "Nhân vị tăng từ giã ra đi, Sư bảo:  - Xà-lê đi ra ngoài, chợt có người hỏi có thấy Triệu Châu chăng, ông làm sao  đối đáp?"),
        ("云：只可道見。", "Tăng thưa:  - Chỉ nói có gặp."),
        ("師云：老僧是一頭驢，你作麼生見？", "Sư bảo:  - Lão tăng là một con lừa, ông làm sao gặp?"),
        ("僧無語。", "Tăng không đáp được."),
        ("師問新到：從什麼處來？", "Sư hỏi một vị tăng mới đến: “Từ đâu đến đây?”"),
        ("云：南方來。", "Tăng thưa: “Từ phương nam đến”."),
        ("師云：還知有趙州關麼？", "- Lại biết có cổng châu Triệu chăng?"),
        ("云：須知有不涉關者。", "- Thầy biết có kẻ chẳng qua khỏi cổng chăng?"),
        ("師叱云：者販私鹽漢！ 又云：兄弟！ 趙州關也難過。", "Sư quát to bảo:  - Gã bàn muối lậu này! Lại bảo tiếp:  - Huynh đệ! Cổng châu Triệu cũng khó qua."),
        ("云：如何是趙州關？ 師云：石橋是。", "- Thế nào là cổng châu Triệu? - Cầu đá."),
        ("有僧從雪峯來，師云：上座莫住此間，老僧者裏只是避難所在，佛法盡在南方。", "Có vị tăng từ Tuyết Phong đến, Sư bảo:  - Thượng tọa chớ trụ trong đây. Chỗ lão tăng ở đây chỉ là chỗ lánh nạn. Phật  pháp trọn ở phương nam."),
        ("云：佛法豈有南北？", "Tăng thưa:  - Phật pháp há có nam bắc sao?"),
        ("師云：直饒你從雪峯，雪峯來也只是箇擔板漢。", "- Dù cho ông đến từ Tuyết Phong và Vân Cư, ông cũng chỉ là kẻ vác bảng."),
        ("云：未審那邊事如何？", "- Con chưa hiểu việc bên kia thế nào?"),
        ("師云：你因甚夜來尿床？", "- Ông nhân gì ban đêm đến đái trên giường?"),
        ("云：達後如何？ 師云：又是屙屎。", "- Sau khi thấu suốt thì thế nào? - Lại là ỉa cứt."),
        ("示眾云：我此間有出窟師子，亦有在窟師子，只是難得師子兒。", "Sư dạy chúng: “Ở chỗ ta ở có sư tử ra khỏi hang, cũng có sư tử ở trong  hang. Chỉ là khó được sư tử con”."),
        ("時有僧彈指對之，師云：是什麼？", "Lúc đó có vị tăng khảy tay để đáp thoại. Sư bảo:  - Là gì?"),
        ("云：師子兒。", "- Sư tử con."),
        ("師云：我喚作師子兒，早是罪過，你更行趯踏。", "- Ta gọi sư tử con, sớm là tội lỗi rồi. Ông có thể nhảy một bước khác nữa  chăng?"),
        ("師問新到：離什麼處？ 云：離雪峯。", "Sư hỏi vị tăng mới đến:  - Từ đâu đến? Tăng thưa:  - Từ Tuyết Phong đến."),
        ("師云：雪峯有什麼言句示人？", "- Tuyết Phong có lời gì dạy người?"),
        ("云：和尚尋常道：盡十方世界是沙門一隻眼。 你等諸人向什麼處屙？ 師云：闍黎若迴，寄箇鍬子去。", "- Hòa thượng thường nói: ‘Trọn mười phương thế giới là một con mắt của sa  môn, mọi người các ông nhằm chỗ nào ỉa?’ - Xà-lê nếu trở lại nơi ấy, hãy cầm cái xẻng này theo"),
        ("師因捨衣俵大眾次，僧便問：和尚總捨却了，用箇什麼去？ 師召云：湖州子。", "Nhân Sư đang xả y chia cho đại chúng, có vị tăng liền hỏi: “Hòa thượng  xả hết cho đại chúng, vậy dùng cái gì?” Sư gọi bảo:   - Kẻ châu Hồ!"),
        ("僧應諾，師云：用箇什麼？", "Tăng ứng thinh:    - Dạ! Sư bảo:  - Ông đang dùng cái gì?"),
        ("師示眾云：未有世界，早有此性。 世界壞時，此性不壞。", "Sư dạy chúng: “Chưa có thế giới, sớm có tánh này; khi thế giới hoại, tánh  này chẳng hoại”.")
    ]

    block_11 = [
        ("師云：你披衲衣來否？", "Sư bảo: - Ông có khoác nạp y chăng?"),
        ("云：披來。", "- Có khoác."),
        ("師云：莫惑我。", "- Chớ lừa ta."),
        ("云：如何得不惑去？", "- Làm sao để chẳng lừa thầy?"),
        ("師云：自作活計，莫取老僧語。", "- Ta tự tạo kế sống, chớ nhận đùa lời của lão tăng."),
        ("師問座主：所習何業？", "Sư hỏi tọa chủ:  - Ðã quen sự nghiệp (tu pháp môn) gì?"),
        ("云：講維摩經。", "Tọa chủ thưa:  - Giảng kinh Duy-ma."),
        ("師云：那箇是維摩祖父？ 云：某甲是。", "- Ai là tác giả của kinh? - Chính là con."),
        ("師云：為什麼却為兒孫傳語？ 主無對。", "- Vì sao ông lại truyền cho con cháu? Tọa chủ không đáp được."),
        ("師一日上堂，僧纔出禮拜，師乃合掌珍重。", "Một hôm Sư thượng đường, vị tăng bước ra vừa lễ bái, Sư bèn chắp tay kính  chào và lui gót."),
        ("又一日，僧禮拜，師云：好好。", "Lại một hôm khác, tăng lễ bái, Sư bảo:  - Khéo khéo hỏi."),
        ("問云：如何是禪？", "- Thế nào là thiền?"),
        ("師云：今日天陰不答話。", "- Hôm nay trời mát chẳng đáp thoại."),
        ("問新到：從何方來？ 云：無方面來。", "Sư hỏi vị tăng mới đến:   - Từ phương nào đến? Tăng thưa:   - Không phía nào đến."),
        ("師乃轉背，僧將坐具隨師轉，師云：大好無方面。", "Sư bèn xoay ngược lưng phía vị tăng. Tăng lấy tọa cụ và xoay theo Sư. Sư bảo:  - Rất tốt, không phía nào."),
        ("問新到：從什麼處來？ 云：南方來。", "Sư hỏi vị tăng khác mới đến: “Từ nơi nào đến đây?” Tăng thưa: “Từ phương nam đến”."),
        ("師云：三千里外逢莫戲。 云：不曾。", "- Ngoài ba ngàn dặm gặp nhau, chớ đùa với ta. - Con chẳng hiểu."),
        ("師云：摘楊花，摘楊花。", "- Nhặt cành dương liễu, nhặt cành dương liễu."),
        ("豐干到五臺山下，見一老人，干云：莫是文殊也無？", "Phong Can đi đến Ngũ Ðài, thấy một ông già ở dưới núi. Phong Can nói:   - Phải là Văn-thù hay không?"),
        ("老人云：不可有二文殊也。", "Ông già đáp:   - Chẳng thể có hai Văn-thù."),
        ("干便禮拜，老人不見。", "Phong Can liền lễ bái, ông già ẩn mất."),
        ("有僧舉似師，師云：豐干只具一隻眼。", "Có vị tăng thuật lại với Sư, Sư bảo: “Phong Can chỉ đủ một con mắt”."),
        ("師乃令文遠作老人，我作豐干，師云：莫是文殊也無？", "Sư bèn sai bảo Văn Viễn hãy làm ông già và Sư làm Phong Can. Sư nói: “Phải là Văn-thù hay không?”"),
        ("遠云：豈有二文殊也？", "Văn Viễn thưa: “Há có hai Văn-thù?”"),
        ("師云：文殊，文殊。", "Sư bảo: “Văn-thù! Văn-thù!”")
    ]

    block_12 = [
        ("師云：院主。", "Sư gọi: “Viện chủ!”"),
        ("院主應諾，師云：喫茶去。", "Viện chủ ứng thinh: “Dạ!” Sư bảo: “Uống trà đi”."),
        ("師到雲居，雲居云：老老大大，何不覓箇住處？", "Sư đến Vân Cư. Vân Cư bảo: “Tuổi đã cao, sao chẳng tìm một chỗ  trụ?”")
    ]

    block_13 = [
        ("師一日將拄杖上茱萸法堂上，東西來去，萸云：作什麼？", "Một hôm Sư cầm gậy đi lên pháp đường, đi từ đông sang tây. Thù Du bảo: “Làm gì?”"),
        ("師云：探水。 萸云：我者裏一滴也無，探箇什麼？ 師將杖子倚壁便下去。", "Sư đáp: “Dò nước”. Thù Du bảo: “Ta ở đây một giọt cũng không có, dò cái gì?” Sư cầm gậy tựa vách rồi ra đi."),
        ("臺山路上有一婆子要問僧，僧問：臺山路向什麼處去？", "Trên đường đi Ðài Sơn có bà già thường tiếp đón và hỏi các vị tăng đến  đó. Một vị tăng hỏi: “Ðường Ðài Sơn đi về hướng nào?”"),
        ("云：驀直去。 僧纔行，婆云：又與麼去也。", "Bà bảo: “Cứ đi thẳng”. Tăng vừa đi, bà bảo: “Lại một người nữa đi như thế”."),
        ("師聞便去問：臺山路向什麼處去？", "Sư nghe kể việc này, liền đi đến hỏi bà lão:  - Ðường Ðài Sơn đi về hướng nào?"),
        ("云：驀直去。 師纔行，婆云：又與麼去也。", "Bà bảo:  - Cứ đi thẳng. Sư vừa đi, bà bảo:  - Lại một người nữa đi như thế."),
        ("師歸舉似大眾云：婆子被老僧勘破了也。", "Sư trở về thuật lại với đại chúng và bảo:  - Bà già bị lão tăng khám phá xong rồi."),
        ("師見僧來，挾火示之云：會麼？", "Sư thấy vị tăng đến, đưa cây gắp lửa lên chỉ cho ông và bảo: “Lãnh hội  chăng?”"),
        ("僧云：不會。", "Tăng thưa: “Chẳng lãnh hội”."),
        ("師云：你不得喚作火，老僧道了也。", "Sư bảo: “Ông chẳng được gọi đó là ‘lửa’. Phần lão tăng đã nói xong rồi”."),
        ("師挾起火云：會麼？", "Sư lại đưa cây gắp lửa lên bảo: “Lãnh hội chăng?”"),
        ("云：不會。", "Tăng thưa: “Chẳng lãnh hội”.")
    ]

    block_14 = [
        ("師又云：且釘者一縫。", "Sư lại bảo: “Hãy đóng đinh một kẽ hở này”."),
        ("師因行路次，見一婆子問：和尚住在什麼處？", "Nhân Sư đang đi đường, gặp một bà già hỏi: “Hòa thượng trụ ở đâu?”"),
        ("師云：趙州東院西。", "Sư đáp: “Phía tây của Ðông Viện ở châu Triệu”."),
        ("師舉問僧云：你道使那箇西字？", "Sư thuật lại việc này và hỏi tăng: “Ông hãy nói ta dùng chữ “tây” nào?”"),
        ("一僧云：東西字。", "Một vị tăng đáp:  - Chữ “tây” của phía đông và tây."),
        ("一僧云：依栖字。", "Một vị tăng khác đáp:  - Chữ “tây” của nương ở."),
        ("師云：你兩人總作得鹽鐵判官。", "Sư bảo:  - Hai người thảy làm được vị quan bán muối và sắt."),
        ("師與侍郎遊園，見兔走過，侍郎問：和尚是大善知識，兔子見為什麼走？", "Sư cùng quan thị lang đi dạo vườn, gặp con thỏ chạy qua. Thị lang hỏi:  “Hòa thượng là đại thiện tri thức, khi con thấy hòa thượng vì sao con thỏ chạy?”"),
        ("師云：老僧好殺。", "Sư bảo: “Lão tăng ưa giết”."),
        ("師因見僧掃地次，遂問：與麼掃還得淨潔也無？", "Nhân Sư thấy vị tăng đang quét đất, bèn hỏi:  - Quét như thế có được sạch sẽ hay không?"),
        ("云：轉掃轉多。", "Tăng thưa:  - Càng quét càng phải quét thêm."),
        ("師云：豈無撥塵者也？", "Sư bảo: - Làm sao mà không có một kẻ trừ bụi?"),
        ("云：誰是撥塵者？", "Tăng thưa: - Ai là kẻ trừ bụi?"),
        ("師云：會麼？ 云：不會。", "Sư bảo: - Lãnh hội chăng? Tăng thưa: - Chẳng lãnh hội."),
        ("師云：問取雲居去。", "Sư bảo: - Hãy đi hỏi Vân Cư."),
        ("其僧乃去問雲居：如何是撥塵者？", "Vị tăng ấy đi hỏi Vân Cư:  - Thế nào là kẻ trừ bụi?"),
        ("雲居云：者瞎漢。", "Vân Cư bảo:  - Gã mù đó!"),
        ("師問僧：你在此間多少時也？", "Sư hỏi vị tăng:  - Ông ở đây bao lâu rồi?"),
        ("僧云：七八年。", "Tăng thưa:  - Da, bảy mươi tám năm."),
        ("師云：還見老僧麼？ 云：見。", "Sư bảo: - Có thấy lão tăng chăng? Tăng thưa: - Dạ thấy."),
        ("師云：我作一頭驢，你作麼生見？", "Sư bảo: - Ta làm con lừa, ông làm sao thấy?"),
        ("云：入法界見。", "Tăng thưa: - Vào pháp giới thì thấy."),
        ("師云：我將為你有此一著，枉喫了如許多飯。", "Sư bảo: - Theo ta biết, ông chỉ đáp có một bên, ăn bao nhiêu cơm thật uổng."),
        ("僧云：請和尚道。", "Tăng thưa: - Thỉnh hòa thượng nói."),
        ("師云：因什麼不道向草料裏見？", "Sư bảo: - Tại sao ông chẳng nói ‘Thấy hòa thượng khi nhìn trong máng cỏ’?")
    ]

    block_15 = [
        ("有俗行者到院燒香，師問僧：伊在那裏燒香禮拜？ 我又共你在者裏語話，正與麼時生在那頭？", "Có vị cư sĩ tại gia đến viện thắp hương, Sư hỏi vị tăng:  -Y ở đằng kia thắp hương lễ bái, ta với ông ở đây nói năng. Chính ngay đây,  sanh ở đằng kia phải không?"),
        ("僧云：和尚是什麼？ 師云：與麼即在那頭也。 云：與麼是先也。 師笑之。", "Tăng thưa:  - Hòa thượng là gì? Sư bảo: - Nếu vậy là sanh ở đằng kia. Tăng thưa: - Nếu như thế là kiểu trước rồi. Sư cười."),
        ("師與小師文遠論義：不得占勝，占勝者輸餬餅。", "Sư cùng Văn Viễn luận nghĩa mà chẳng được thắng cuộc là kết luận sau  cùng, người thắng cuộc sẽ thua một cái bánh nướng."),
        ("師云：我是一頭驢。", "Sư bảo: “Ta là một con lừa”."),
        ("遠云：我是驢。", "Viễn nói: “Con là yên cương của lừa”."),
        ("師云：我是驢糞。", "Sư bảo: “Ta là phân lừa”."),
        ("遠云：我是糞中虫。", "Viễn nói: “Con là con giòi trong phân”."),
        ("師云：你在彼中作麼？", "- Ông ở trong đó làm gì?"),
        ("遠云：我在彼中過夏。", "- Con ở trong đó qua hạ."),
        ("師云：把將餬餅來。", "- Hãy đem bánh nướng đến đây."),
        ("師因入內迴，路上見一幢子無一截，僧問云：幢子一截，上天去也？ 入地去也？", "Nhân Sư vào trong cung trở về, thấy một trụ đá khắc kinh mất một đoạn. Tăng hỏi:  - Một đoạn của trụ đá bay lên trời hay xuống địa ngục?"),
        ("師云：也不上天，也不入地。", "Sư bảo:  - Cũng chẳng bay lên trời, cũng chẳng xuống địa ngục."),
        ("云：向什麼處去？", "- Ði về đâu?"),
        ("師云：撲落也。", "- Rơi đổ rồi."),
        ("師坐次，一僧纔出禮拜，師云：珍重！", "Sư đang ngồi, tăng vừa bước đến định hỏi, Sư bảo:  - Cám ơn sự bối rối của ông!"),
        ("僧伸問次，師云：又是也。", "Tăng đang tỏ bày thưa hỏi, Sư bảo:  - Còn nữa à?"),
        ("師因在簷前立，見燕子語，師云：者燕子喃喃地招人言語。", "Một hôm Sư đứng trước rèm nghe chim én kêu. Sư bảo:  - Chim én chiếp chiếp là gọi người để nói năng."),
        ("僧云：未審他還甘也無？", "Tăng thưa:  - Con chưa hiểu, có phải chúng có tác ý hay không?"),
        ("師云：依稀似曲纔堪聽，又被風吹別調中。", "Sư bảo: - Lờ mờ nghe tợ khúc ca, gió hiu hiu thổi riêng là điệu ngâm."),
        ("有僧辭去，師云：什麼處去？", "Có vị tăng từ giã đi nơi khác, Sư bảo:  - Ði đâu?"),
        ("云：閩中去。", "Tăng thưa:  - Ði Mân Trung (Phúc kiến)."),
        ("師云：閩中大有兵馬，你須迴避。", "Sư bảo: - Mân Trung nhiều lính tráng, ông làm sao né tránh?"),
        ("云：向甚處迴避？ 師云：恰好。", "- Nhằm chỗ nào né tránh? - Khéo hợp đấy."),
        ("有僧上參次，見師衲衣蓋頭坐次，僧便退，師云：闍黎莫道老僧不祇對。", "Có vị tăng đang đi đến để thưa hỏi, thấy Sư đang ngồi lấy nạp y trùm đầu,  liền lui gót. Sư bảo:  - Xà-lê chớ bảo lão tăng chẳng đối đáp nhe!"),
        ("師問僧：從什麼處來？", "Sư hỏi vị tăng:   - Từ đâu đến đây?"),
        ("云：南方來。", "Tăng thưa:   - Từ phương nam đến."),
        ("師云：共什麼人為伴？", "- Cùng với người nào làm bạn?"),
        ("云：水牯牛。", "- Con trâu nước."),
        ("師云：好箇師僧！ 因什麼與畜生為伴？", "- Ông là một ông tăng tốt, nhân gì cùng súc sanh làm bạn?"),
        ("云：不異故。", "- Vì chẳng khác."),
        ("師云：好箇畜生！ 云：爭肯？", "- Ông là một súc sanh tốt. - Chẳng nhận."),
        ("師云：不肯且從，還我伴來。", "- Chẳng nhận thì tùy, hãy đến đây và chọn ta làm bạn thay vì con trâu nước."),
        ("師問僧：堂中還有祖師也無？ 云：有。", "Sư hỏi vị tăng: “Trong tăng đường có tổ sư (Đạt-ma) hay không?” Tăng thưa: “Có”."),
        ("師云：喚來與老僧洗脚。", "Sư bảo: “Gọi đến rửa chân cho lão tăng”."),
        ("堂中有二僧相推，不肯作第一座，主事白和尚，師云：總教他作第二座。", "Trong tăng đường có hai vị tăng nhường nhau chẳng chịu làm đệ nhất tòa. Chủ sự bạch với Sư. Sư bảo:  - Thảy bảo họ làm đệ nhị tòa."),
        ("云：教誰作第一座？", "Chủ sự hỏi:  - Vậy bảo ai làm đệ nhất tòa?"),
        ("師云：裝香著。", "Sư bảo: - Thắp hương đi."),
        ("云：裝香了也。 師云：戒香？ 定香？", "Chủ sự thưa: - Hương thắp rồi. Sư bảo: - Hương giới, hương định."),
        ("師問僧：離什麼處？", "Sư hỏi vị tăng: “Rời chỗ nào?”"),
        ("云：離京中。", "Tăng thưa: “Lìa kinh đô“."),
        ("師云：你還從潼關過麼？", "Sư bảo: - Ông có đi qua Ðồng Quan chăng?"),
        ("云：不歷。 師云：今日捉得者販私鹽漢。", "Tăng thưa: - Chẳng đi qua. Sư bảo: - Hôm nay bắt được gã bán muối lậu này.")
    ]

    block_16 = [
        ("方到三門下，師云：又道大王來也。", "Sư bảo: “Chính ông nói đại vương đến”."),
        ("因上東司召文遠，文遠應諾，師云：東司上不可與你說佛法也。", "Nhân Sư lên nhà xí, gọi Văn Viễn, Văn Viễn ứng thinh:  - Dạ! Sư bảo:  - Trong nhà xí chẳng thể nói Phật pháp với ông."),
        ("因在殿上過，乃喚侍者，侍者應諾，師云：好一殿功德。", "Nhân Sư đi ngang qua cung điện nhà vua, bèn gọi thị giả. Thị giả ứng  thinh: “Dạ!” Sư bảo: “Một điện công đức tốt”."),
        ("侍者無對。", "Thị giả không đáp được."),
        ("師因到臨濟，方始洗脚，臨濟便問：如何是祖師西來意？ 師云：正值洗脚。", "Sư đến Lâm Tế. Đang lúc Sư rửa chân Lâm Tế hỏi:  - Thế nào là ý tổ sư từ tây sang? Sư đáp:  - Ngay đây ta đang rửa chân."),
        ("臨濟乃近前側聆，師云：若會便會，若不會更莫㗖 拂袖去。", "Lâm Tế bèn đến gần nghiêng tai như thể chưa nghe rõ. Sư nói:  - Nếu hội liền hội. Nếu chẳng hội chớ nhai lại nữa. Ông phải làm sao? Lâm Tế phất tay áo ra đi."),
        ("師云：三十年行脚，今日為人錯下注脚。", "Sư nói:  - Ba mươi năm đi hành cước, hôm nay lầm giải thích cho người bỏ mặc ngoài  tai."),
        ("師因到天台國清寺，見寒山．拾得，師云：久嚮寒山．拾得到來，只見兩頭水牯牛。", "Nhân Sư đến chùa Quốc Thanh ở Thiên Thai gặp Hàn Sơn và Thập Ðắc,  Sư nói:  - Ðã lâu nghe tiếng Hàn Sơn và Thập Ðắc, đến đây chỉ thấy hai con trâu nước."),
        ("寒山．拾得便作牛鬬，師云：叱！ 叱！", "Hàn Sơn và Thập Ðắc liền làm trâu đấu nhau. Sư quát lên!"),
        ("寒山．拾得咬齒相看，師便歸堂。", "Hàn Sơn và Thập Ðắc nghiến răng nhìn nhau. Sư liền trở về tăng đường.")
    ]

    block_17 = [
        ("師云：沙彌童行得入門，侍者在門外。", "Sư bảo:    - Sa-di đồng hạnh được vào cửa, còn thị giả ở ngoài cửa."),
        ("師行脚時到一尊宿院，纔入門相見，便云：有麼？ 有麼？", "Lúc Sư đi hành cước đến viện của một vị tôn túc, vừa vào cửa gặp nhau  liền nói: “Có chăng? Có chăng?”"),
        ("尊宿竪起拳頭，師云：水淺船難泊。 便出去。", "Tôn túc giơ nắm tay lên. Sư nói: “Nước cạn thuyền khó ghé”. Rồi đi ra."),
        ("又到一院，見尊宿便云：有麼？ 有麼？", "Sư lại đến một viện khác, gặp tôn túc liền nói:  - Có chăng? Có chăng?"),
        ("尊宿竪起拳頭，師云：能縱能奪，能取能撮。 禮拜便出去。", "Tôn túc giơ nắm tay lên. Sư nói:  - Ông tha (cứu) hay đoạt (giết) đều được. Sư lễ bái rồi đi ra."),
        ("師一日拈數珠問新羅長老：彼中還有者箇也無？", "Một hôm Sư đưa xâu chuỗi lên hỏi trưởng lão Tân La:  - Chỗ ông ở có cái này hay không?"),
        ("云：有。", "Trưởng lão đáp:  - Có."),
        ("師云：何似者箇？", "- Có giống cái này không?"),
        ("云：不似者箇。", "Trưởng lão thưa: - Chẳng giống cái này."),
        ("師云：既有，為什麼不似？", "- Ðã có, vì sao chẳng giống?"),
        ("無語。", "Trưởng lão không lời đáp."),
        ("師自代云：不見道新羅大唐？", "Sư tự đáp thay:  - Sao ông không nói ‘Tân La, Ðại Ðường’."),
        ("問新到：什麼處來？", "Sư hỏi vị tăng mới đến:  - Ở đâu đến?"),
        ("云：南方來。", "Tăng thưa:  - Từ phương nam đến."),
        ("師竪起指云：會麼？ 云：不會。", "Sư đưa ngón tay lên hỏi:  - Lãnh hội chăng? Tăng thưa:  - Chẳng lãnh hội."),
        ("師云：動止萬福。 不會。", "Sư bảo: - Ngay cả câu ‘Xin chào, khỏe không?’ ông cũng chẳng lãnh hội."),
        ("師行脚時問大慈：般若以何為體？", "Lúc Sư đi hành cước hỏi Ðại Từ: “Bát nhã lấy gì làm thể?”")
    ]

    block_18 = [
        ("師云：我與你隔海。", "Sư bảo: “Ta cùng ông cách biển”."),
        ("問僧：什麼處來？ 云：雲居來。", "Sư hỏi tăng: “Ở đâu đến đây?” Tăng thưa: “Ở Vân Cư đến”."),
        ("師云：雲居有什麼言句？", "- Vân Cư có lời gì chỉ dạy?"),
        ("云：有僧問：羊掛角時如何？ 雲居云：六六三十六。", "Tăng nói: “Có vị tăng hỏi khi linh dương treo sừng thì thế nào?” Vân Cư đáp: “Sáu lần sáu ba mươi sáu”."),
        ("師云：雲居師兄猶在。", "- Sư huynh Vân Cư vẫn còn đây."),
        ("僧却問：未審和尚尊意如何？", "Tăng hỏi lại Sư:  - Chưa biết tôn ý hòa thượng thế nào?"),
        ("師云：九九八十一。", "Sư đáp:  - Chín lần chín tám mươi mốt."),
        ("有一婆子日晚入院來，師云：作什麼？ 婆云：寄宿。", "Có một bà già chiều tối vào viện. Sư hỏi: “Làm gì?” Bà đáp: “Ngủ nhờ”."),
        ("師云：者裏是什麼所在？ 婆呵呵大笑而去。", "Sư bảo:  - Ở đây là chỗ nào? Bà cười to ha hả liền đi ra."),
        ("師出外，逢見一箇婆子提一箇籃子，師便問：什麼處去？ 云：偷趙州笋去。", "Sư đi ra ngoài gặp một bà già tay xách một cái giỏ. Sư liền hỏi:  - Ði đâu đó? Bà đáp:  - Ði trộm măng của Triệu Châu."),
        ("師云：忽見趙州又作麼生？ 婆子近前打一掌。", "Sư bảo:  -Chợt gặp Triệu Châu thì làm sao? Bà đến gần tát Sư một tát."),
        ("師因見院主送生飯，鵶子見便總飛去，師云：鵶子兒見你，為什麼却飛去？ 院主云：怕某甲。", "Một hôm Sư thấy viện chủ cúng cơm xuất sanh, quạ thấy liền bay đi hết. Sư bảo: “Con quạ thấy ông, vì sao lại bay đi?” Viện chủ thưa: “Nó sợ con”."),
        ("師云：是什麼語話？ 師代云：為某甲有殺心在。", "Sư bảo: - Ông đang nói gì thế? Sư đáp thay:  - Vì con còn có tâm sát."),
        ("師問僧：什麼處來？ 云：江西來。", "Sư hỏi tăng: - Ở đâu đến đây? Tăng thưa:  - Ở Giang Tây đến."),
        ("師云：趙州著在什麼處？ 僧無對。", "- Tìm Triệu Châu ở chỗ nào? Tăng không đáp được."),
        ("師從殿上過，見一僧禮拜，師打一棒云：禮拜也是好事。", "Sư rời điện đường, thấy một vị tăng đang lễ bái. Sư đánh một gậy. Tăng  thưa: “Lễ bái cũng là một việc tốt”."),
        ("師云：好事不如無。", "Sư bảo: “Một việc tốt không tốt bằng không một việc”."),
        ("師因參潼關，潼關問師云：你還知有潼關麼？ 師云：知有潼關。", "Nhân Sư đến Ðồng Quan. Người gát Ðồng Quan hỏi Sư:  - Ông có biết ông đang ở Ðồng Quan hay không? Sư đáp:  - Biết."),
        ("云：有公驗者即得過，無公驗者不得過。", "Người gát bảo:  -. Ai có giấy chứng minh thì đi qua; không giấy chứng minh thì chẳng được  qua."),
        ("師云：忽遇鑾駕來時如何？ 關云：也須檢點過。", "- Bỗng khi xe của vua đến thì sao? - Cũng cần phải kiểm tra mới cho qua."),
        ("云：你要造反。", "- Vậy là ông muốn tạo phản."),
        ("師到寶壽，寶壽見師來，遂乃背面而坐，師便展坐具， 寶壽起立，師便出去。", "Sư đến Bảo Thọ. Bảo Thọ thấy Sư đến, bèn ngồi quay lưng lại. Sư liền trải tọa cụ, Bảo Thọ đứng  dậy, Sư liền đi ra."),
        ("師在南泉時，泉牽一頭水牯牛入僧堂內，巡堂而轉，首座乃向牛背上三拍，泉便休去。", "Lúc Sư ở Nam Tuyền, Nam Tuyền dẫn con trâu đực vào trong tăng đường  đi vòng quanh. Thủ tọa bèn vỗ lên lưng trâu ba cái, Nam Tuyền liền thôi nghỉ."),
        ("師後將一束草安首座面前，首座無對。", "Sau Sư đem một bó cỏ bỏ vào miệng rồi đứng trước mặt thủ tọa. Thủ tọa không  đáp được.")
    ]

    block_19 = [
        ("有無不是說，去來非去來。 為你說難法，對面識得來。", "Có không chẳng nói đó, Ðến đi chẳng đến đi. Vì ông nói pháp nạn, Ðối diện biết được ngay. (Ðối diện thức đắc lai.)"),
        ("偈頌 十二時歌十二時歌 鷄鳴丑，愁見起來還漏逗。 裙子褊衫箇也無，袈裟形相些些有。", "Khúc Ca 12 Giờ: Gà gáy Sửu, Biết buồn lận đận rồi thức dậy. Áo trong quần ngắn một cũng không. Hình tướng ca sa có chút ít."),
        ("裩無，袴無口，頭上青 行利濟人，誰知變作不唧溜。", "Quần không lưng, khố không miệng. Trên đầu tro xanh năm ba đấu. Mong mỏi tu hành lợi giúp người, Ai ngờ trái lại thành kẻ ngu."),
        ("平旦寅，荒村破院實難論。 解齋粥米全無粒，空對閑窻與隙塵。", "Rạng đông Dần. Thôn vắng viện hoang thật khó bàn. Cháo cơm toàn thảy không chút gạo, Luống đối song nhàn với khích trần."),
        ("唯，家憎愛斷，思量不覺淚沾巾。", "Chỉ sẻ kêu, không người thân thích, Riêng ngồi nghe mãi lá rụng rơi. Ai bảo xuất gia cắt yêu ghét? Nghĩ suy bất chợt lệ ướt khăn!"),
        ("日出卯，清淨却翻為煩惱。 有為功德被塵幔，無限田地未曾掃。", "Trời mọc Mão. Thanh tịnh lại thành ra phiền não. Công đức hữu vi bị trần che, Ruộng đất không cùng đâu quét sạch?"),
        ("攢眉多，稱心少，尀耐東村黑黃老。 供利不曾將得來，放驢喫我堂前草。", "Nhíu mày nhiều mà xứng tâm ít. Khó chịu thôn đông lão Hoàng Hắc. Lợi cúng chẳng từng đem đến dâng, Trước nhà ta thả lừa ăn cỏ."),
        ("食時辰，煙火徒勞望四鄰。 饅頭䭔子前年別，今日思量空嚥津。", "Giờ ăn Thìn. Bếp lửa nhọc công ngóng bốn bên. Bánh bao bánh hấp năm qua biệt, Hôm nay nghĩ lại nuốt miếng suông."),
        ("持念少，嗟歎頻，一百家中無善人。 來者祇道覓茶喫，不得茶噇去又嗔。", "Gìn niệm ít, than thở thường. Trong cả trăm nhà không kẻ lành. Người đến đây chỉ tìm trà uống, Chẳng được uống trà lại nổi sân."),
        ("禺中巳，削髮誰知到如此。 無端被請作村僧，屈辱飢悽受欲死。", "Gần trưa Tỵ. Cắt tóc ai ngờ đến như thế? Chợt đâu bị thỉnh làm thôn tăng. Nhục oan đói khổ chịu vô kể."),
        ("胡張三，黑李四，恭敬不曾生些子。 適來忽爾到門頭，唯道借茶兼借紙。", "Hồ Trương Tam, Hắc Lý Tứ, Chẳng từng chút nào sanh cung kính. Vừa rồi bỗng chợt đến cửa đây, Chỉ nói mượn trà cùng mượn giấy."),
        ("日南午，茶飯輪還無定度。 行却南家到北家，果至北家不推註。", "Nhật nam Ngọ. Cơm trà cứ thế xoay vần mãi. Nhà nam nhà bắc hành cước sang, Quả đến nhà bắc chẳng thêm giải."),
        ("苦沙鹽，大麥醋，蜀黍米飯虀萵苣。 唯稱供養不等閑，和尚道心須堅固。", "Muối hạt thô cùng giấm đại mạch, Rau, dưa muối, gạo cơm nếp thục. Chỉ xứng cúng dường chẳng tầm thường, Hòa thượng đạo tâm cần vững chắc."),
        ("日昳未，者回不踐光陰地，曾聞一飽忘百飢，今日老僧身便是。", "Trời xế Mùi. Lần này chẳng đạp bóng thời gian. Từng nghe một no quên trăm đói, Chính đó hiện nay thân lão tăng."),
        ("不習禪，不論義，鋪箇破蓆日裏睡，想料上方兜率天，也無如此日炙背。", "Chẳng tập thiền, chẳng luận nghĩa. Trải manh chiếu rách giữa ngày ngủ. Toan tính vượt trên Ðâu Suất thiên, Chẳng tốt gì mặt trời nướng lưng."),
        ("晡時申，也有燒香禮拜人。 五箇老婆三箇癭，一雙面子黑皴皴。", "Xế chiều Thân. Cũng người lễ bái với thắp hương. Năm bà lão già, ba cục bướu (cổ) Một đôi gương mặt nhăn nhúm đen."),
        ("油麻茶，實是珍，金剛不用苦張筋。 願我來年蠶麥熟，羅睺羅兒與一文。", "Trà dầu mè, quý gì hơn! Kim Cang chẳng dùng nhọc sức làm. Nguyện ta năm tới tằm mạch chín, La-hầu-la con cho một lời."),
        ("日入酉，除却荒涼更何守。 雲水高流定委無，歷寺沙彌鎮常有。", "Trời vào Dậu. Trừ chỗ hoang vu còn đâu giữ? Cao tăng lưu chuyển không buộc ràng. Từng chùa Sa-di vẫn hằng hữu."),
        ("出格言，不到口，枉續牟尼子孫後。 一條拄杖麤楋藜，不登山兼打狗。", "Lời xuất cách chẳng đến miệng, Cháu con tiếp nối Mâu Ni uổng. Một chiếc gậy lê thô xấu thôi, Chẳng những lên non còn đánh chó."),
        ("黃昏戌，獨坐一間空暗室。 陽燈光永不逢，眼前純是金州漆。", "Hoàng hôn Tuất. Một mình ngồi giữa nhà trống tối. Mãi vắng ánh đèn sáng lung linh. Trước mắt một màu đen như mực."),
        ("鐘不聞，虗度日，唯聞老鼠閙啾唧。 憑何更得有心情，思量念箇波羅蜜。", "Chuông chẳng nghe, ngày trôi qua, Chít chít chỉ riêng nhộn tiếng chuột. Còn đâu lại có được tâm tình? Nghĩ suy một niệm Ba-la-mật."),
        ("人定亥，門前明月誰人愛。 向裏唯愁臥去時，勿箇衣裳著甚蓋。", "Người định Hợi. Trước cửa sáng trăng ai thích nhỉ? Chỉ buồn trong ấy lúc nằm đây, Không cái áo quần che mặc kỹ."),
        ("劉維那，趙五戒，口頭說善甚奇怪。 任你山僧囊罄空，問著都緣總不會。", "Ngoài áo che thân, cần gì nữa? Lưu Duy-na, Triệu ngũ giới, Miệng nói điều lành thật lạ kỳ! Mặc ông tăng núi đảy trống trơn, Hỏi đến hoàn toàn chẳng hội thảy."),
        ("半夜子，心境何曾得暫止？ 思量天下出家人，似我住持能有幾？", "Nửa đêm Tý. Tâm cảnh đâu từng có tạm nghỉ? Nghĩ đến khắp nơi kẻ xuất gia, Giống ta trụ trì được có mấy?"),
        ("土榻床，破蘆䉬，老榆木枕全無被，尊像不燒安息香，灰裏唯聞牛糞氣。", "Ðất làm giường, chiếu lau rách, Gỗ du làm gối, không mền đắp. Tượng thờ chẳng thắp An Tức hương, Trong tro toàn ngửi phân bò phất."),
        ("見起塔乃有頌見起塔乃有頌 本自圓成，何勞疊石。 名邈雕鐫，與吾懸隔。 若人借問，終不指畫。", "Sư thấy xây tháp bèn có bài tụng: Vốn tự tròn thành, Ðâu nhọc chất đá. Ðá tạc khắc thành, Cùng ta cách xa. Nếu người xin hỏi, Đáp: Không nên vẽ."),
        ("因見諸方見解異途乃有頌因見諸方見解異途乃有頌 趙州南，石橋北，觀音院裏有彌勒。 祖師遺下一隻履，直至如今覓不得。", "Sư thấy các nơi có nhiều kiến giải sai khác, bèn có bài tụng: Nam châu Triệu, bắc cầu đá, Trong viện Quán Âm có Di-lặc. Tổ sư để lại một chiếc giày, Thẳng đến hiện nay tìm chẳng được."),
        ("因魚鼓有頌因魚鼓有頌 四大猶來造化功，有聲全貴裏頭空。 莫怪不與凡夫說，只為宮商調不同。", "Nhân trống mõ có bài tụng: Bốn đại vốn tạo từ hóa công, Có tiếng do trống rỗng bên trong. Lạ chi với phàm phu chẳng nói, Vì bởi cung thương điệu chẳng đồng."),
        ("因蓮花有頌因蓮花有頌 奇異根苗帶雪鮮，不知何代別西天。 淤泥深淺人不識，出水方知是白蓮。", "Nhân hoa sen có bài tụng: Lạ lùng mầm rễ lấp lánh tuyết, Chẳng rõ lúc nào biệt trời Tây. Bùn lầy sâu cạn người chẳng biết, Khỏi nước mới hay sen trắng đây."),
        ("附趙王與師作真贊附趙王與師作真贊 碧溪之月，清鏡中頭。 我師我化，天下趙州。", "Triệu Vương tán hình tượng Sư: Trăng nơi khe biếc, Ðầu trong gương trong. Thầy ta ta hóa, Khắp chốn Triệu Châu."),
        ("哭趙州和尚二首哭趙州和尚二首 師離㴲水動王侯，心印光潛麈尾收，碧落霧霾松嶺月，滄溟浪覆濟人舟。", "Khóc Hòa thượng Triệu Châu. Thầy lìa Tư Thủy động vương hầu, Tâm ấn sáng ngầm phất tử thâu. Trời rộng sương mờ trăng tùng đỉnh, Biển to sóng úp chiếc thuyền phao."),
        ("一燈乍滅波旬喜，雙眼重昏道侶愁，縱是了然雲外客，每瞻瓶几淚還流。", "Một đèn chợt tắt Ba-tuần thích, Ðôi mắt lại mờ bạn đạo sầu. Nếu ai thấu triệt đám mây mù, Hễ thấy ghế bình lệ cũng trào!"),
        ("佛日西傾祖印隳，珠沉丹沼月沉輝，影敷丈室爐烟慘，風起禪堂松韻微。", "Phật nhật về Tây, Tổ ấn suy, Châu chìm ao thắm, nguyệt chìm soi. Bóng trùm trượng thất khói hương thảm, Gió dậy thiền đường tùng reo than."),
        ("隻履乍來留化跡，五天何處又逢歸？ 解空弟子絕悲喜，猶自潸然對雪幃。", "Chiếc dép chợt hiện lưu dấu hóa, Ngũ thiên đâu chỗ gặp về ôi! Hiểu KHÔNG đệ tử vui buồn dứt, Trước màu trắng tự vẫn sụt sùi!")
    ]

    replacements = [
        (156, 158, block_1),
        (303, 311, block_2_3),
        (331, 334, block_4),
        (452, 454, block_5),
        (468, 473, block_6),
        (580, 586, block_7),
        (628, 634, block_8),
        (634, 641, block_9),
        (647, 672, block_10),
        (706, 729, block_11),
        (735, 738, block_12),
        (747, 757, block_13),
        (786, 807, block_14),
        (809, 843, block_15),
        (853, 863, block_16),
        (885, 900, block_17),
        (930, 956, block_18),
        (971, len(orig_pairs), block_19)
    ]

    new_pairs = list(orig_pairs)
    for s, e, blk in sorted(replacements, key=lambda x: x[0], reverse=True):
        new_pairs[s:e] = blk

    # Áp dụng căn chỉnh chi tiết dứt điểm 16 lỗi theo yêu cầu mới
    final_pairs = apply_precise_fixes(new_pairs)

    return final_pairs
