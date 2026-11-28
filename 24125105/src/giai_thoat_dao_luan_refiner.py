"""Module tinh chỉnh chuẩn xác ranh giới câu, trượt chéo nhiều dòng và vệ sinh văn bản
cho tác phẩm Giải Thoát Đạo Luận (解脫道論 - Vimuttimagga, CV09).

Kiến trúc tinh chỉnh 4 tầng (toàn bộ định vị bằng ngữ cảnh nguyên văn - content-anchored):
- Tầng 1: 30 vùng lệch ranh giới hỏi–đáp, lỗi dấu hỏi CBETA và cụm trượt cục bộ (đợt rà soát 1).
- Tầng 2: 10 cụm TRƯỢT CHÉO nhiều dòng ưu tiên (Q2, Q6, Q8, Q10, Q11, Q12 – tối đa 12 dòng liên tiếp).
- Tầng 3: 45 cặp lệch cụm kết câu '此謂X。/是名X。' (3A) và 20 cặp lệch ranh giới 1 vế dạng khác (3B).
- Tầng 4: Chuẩn hóa vệ sinh văn bản tiếng Việt (dính dấu câu, hai dấu chấm, gạch ngang thừa,
          vị trí dấu thanh kiểu cũ lọan/thóat/đọan và các lỗi gõ dấu từ bản in PDF gốc).
"""

import re
from typing import List, Tuple


def _replace_block(
    pairs: List[Tuple[str, str]],
    name: str,
    start_han_prefix: str,
    end_han_suffix: str,
    expected_span: int,
    new_block: List[Tuple[str, str]],
) -> List[Tuple[str, str]]:
    """Tìm khối liên tiếp có chiều dài expected_span khớp đầu–cuối vế Hán và thay thế chuẩn xác."""
    matches = []
    n = len(pairs)
    for i in range(n - expected_span + 1):
        if pairs[i][0].startswith(start_han_prefix) and pairs[i + expected_span - 1][0].endswith(end_han_suffix):
            matches.append(i)
    if len(matches) != 1:
        raise ValueError(
            f"[giai_thoat_dao_luan_refiner] Lỗi định vị khối '{name}': "
            f"tìm thấy {len(matches)} vị trí (kỳ vọng 1) với prefix={start_han_prefix!r}, suffix={end_han_suffix!r}"
        )
    idx = matches[0]
    return pairs[:idx] + new_block + pairs[idx + expected_span:]


def _apply_stage1_initial_30(p: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Tầng 1: 30 khối tinh chỉnh ranh giới câu & hỏi–đáp đợt 1."""
    # 1. Q1 - Phẩm 2 (297–299)
    p = _replace_block(
        p, "S1_01_Q01_P02_297_299",
        "復次有學無學不動法波羅提木叉者，",
        "以此波羅提木叉威儀成就住者，護四威儀。", 3,
        [
            ("復次有學無學不動法波羅提木叉者，是戒是起、是初、是行、是護、是威儀、是脫、是無縛、是諸法面，為正受善法，名波羅提木叉義。",
             "Lại nữa có học, vô học; bất động pháp Ba La Đề Mộc Xoa. Giới nầy là khởi. Việc đầu tiên là hành việc giữ gìn nầy là uy nghi. Sự thoát ra khỏi nầy là không bị trói buộc. Đây là các pháp bề mặt, làm chánh thọ thiện pháp. Gọi nghĩa là Ba La Đề Mộc Xoa."),
            ("不越身口業，是威儀所覆者。",
             "Chẳng vượt khỏi thân, khẩu, nghiệp. Oai nghi nầy bị che giấu."),
            ("以此波羅提木叉威儀成就住者，護四威儀。",
             "Lấy oai nghi Ba La Đề Mộc Xoa nầy thành tựu ở lại. Giữ gìn 4 oai nghi."),
        ],
    )

    # 2. Q2 - Phẩm 3 (603–604)
    p = _replace_block(
        p, "S1_02_Q02_P03_603_604",
        "云何受？", "我從今日斷貪住處受遇得處。", 2,
        [
            ("云何受？遇得處住，", "Thế nào gọi là thọ ngộ đắc xứ trụ?"),
            ("不樂人所貪、不惱他令避，知是過患、見遇得處功德，我從今日斷貪住處受遇得處。",
             "Chẳng vui nơi người tham, chẳng buồn giận người khác làm cho xa lìa. Biết được điều sai trái nầy, thấy chỗ thích hợp có công đức, nên ta từ ngày hôm nay, đoạn lìa chỗ tham ở, thọ chỗ thích hợp."),
        ],
    )

    # 3. Q2 - Phẩm 3 (630–633)
    p = _replace_block(
        p, "S1_03_Q02_P03_630_633",
        "若正食時，見象馬牛蛇、", "方便住聚落，不失無事處。", 4,
        [
            ("若正食時，見象馬牛蛇、雨、和上、闍梨、客比丘來，方便而起，起已更食，不失一坐。",
             "Nếu lúc đang ăn mà thấy voi, ngựa, bò, rắn, Hòa Thượng A Xà Lê khách Tỳ Kheo đến, phương tiện mà qua khỏi, qua khỏi rồi mới ăn, chẳng mất một chỗ ngồi."),
            ("若節量食及時後食，無方便。",
             "Nếu biết lương thực và thời hậu thực không phải là phương tiện."),
            ("云何無事處方便？", "Thế nào gọi là vô sự xứ phương tiện?"),
            ("或為受戒、懺罪、問法、布薩自恣、自病、看疾、問經疑處，如是等緣，方便住聚落，不失無事處。",
             "Hoặc là thọ giới sám tội, vấn pháp, Bố Tát, tự tứ, trị bịnh, khán bịnh. Hỏi rằng: Qua chỗ nghi là thế nào? Như thế các duyên, phương tiện ở trong làng xóm chẳng mất vô sự xứ."),
        ],
    )

    # 4. Q2 - Phẩm 3 (635–636)
    p = _replace_block(
        p, "S1_04_Q02_P03_635_636",
        "若遇雨時宜入覆處，明相既現還而不失樹下。", "常坐不臥無方便。", 2,
        [
            ("若遇雨時宜入覆處，明相既現還而不失樹下。露住、塚間，遇得此等方便，亦復如是，餘住處可住。",
             "Nếu gặp lúc mưa, liền vào núp bóng, khi dứt mưa liền trở lại như cũ mà chẳng mất. Dưới gốc cây, ở chỗ trống trải nơi gò mả, gặp chỗ thích nghi v.v... là phương tiện. Lại cũng như thế. Ngoài trụ xứ có thể ở."),
            ("常坐不臥無方便。", "Thường ngồi chẳng nằm là chẳng phải phương tiện."),
        ],
    )

    # 5. Q2 - Phẩm 3 (638–640)
    p = _replace_block(
        p, "S1_05_Q02_P03_638_640",
        "如毘曇中說八頭陀，是時後不食攝。", "樹下、露坐、塚間，何故於無事處？", 3,
        [
            ("如毘曇中說八頭陀，是時後不食攝。",
             "Như trong Tỳ Đàm nói là 8 loại Đầu Đà. Lúc ấy sau đó chẳng nhiếp về việc ăn."),
            ("節量、一坐，其所受持成一種類，是無事處攝。",
             "Tiết lượng một chỗ ngồi. Việc nầy thọ trì thành một thể loại. Đây gọi là vô sự xứ nhiếp."),
            ("樹下、露坐、塚間，何故於無事處？",
             "Nơi dưới gốc cây, chỗ ngồi trống và gò mả. Vì sao gọi là nơi vô sự?"),
        ],
    )

    # 6. Q2 - Phẩm 5 (844–848): Kết hợp trọn bộ C2 (844–846) + điểm 847–848 thành 1 khối 5 dòng chuẩn xác
    p = _replace_block(
        p, "S1_06_C2_Q02_P05_844_848",
        "答：若知某甲住處是功德成就可重，", "得聞是已深思隨喜，當往彼處親覲受行。", 5,
        [
            ("答：若知某甲住處是功德成就可重，若有禪師應當往彼。",
             "Đáp rằng: Nếu biết nơi ở của người A, B thì công đức thành tựu có thể quý mến. Nếu có Thiền sư nên lui tới kia."),
            ("若自不知、餘處同學知，應往親覲。",
             "Nếu tự chẳng biết chỗ nào của kẻ đồng học; nên tìm đến gần gũi."),
            ("已知時節如法未說其意，恭敬勞問起居，諮訪所行：何處國土何處住止，有眾安住，有僧靜坐，有是禪師，其行若為？",
             "Rồi biết lúc nào như pháp chưa nói ý nầy. Cung kính khơi hỏi khởi cư. Muốn hỏi chỗ hành thì nơi nào nước nào và dừng ở nơi đâu, có chúng an trụ, có tăng tịnh tọa, có cả Thiền sư. Việc làm nầy nếu làm?"),
            ("以何功德一切所貴？應作如是問。",
             "Lấy gì là công đức tất cả chỗ quý; nên làm như thế và hỏi."),
            ("同學應答：某國某住某眾禪坐，某禪師眾所愛重。得聞是已深思隨喜，當往彼處親覲受行。",
             "Đồng học nên đáp rằng: Nước đó, ở chỗ ấy, chúng thiền tọa ấy, Thiền sư ấy v.v... được chúng ái trọng, được nghe điều nầy rồi nghĩ sâu, tùy hỷ, rồi đến chỗ kia thân cận học hỏi thọ lãnh."),
        ],
    )

    # 7. Q3 - Phẩm 6 (938–939)
    p = _replace_block(
        p, "S1_07_Q03_P06_938_939",
        "二界最近故成癡行人，所謂地界、水界。", "二界最近故成瞋行人，所謂火界、風界。", 2,
        [
            ("二界最近故成癡行人，所謂地界、水界。",
             "Hai giới gần gũi vậy, thành si hành nhơn. Đó là địa giới và thủy giới."),
            ("二界最近故成瞋行人，所謂火界、風界。",
             "Hai giới gần gũi, thành sân hành nhơn. Đó là hỏa giới, phong giới."),
        ],
    )

    # 8. Q3 - Phẩm 7 (1052–1053)
    p = _replace_block(
        p, "S1_08_Q03_P07_1052_1053",
        "答：九行處為神通緣，除無色一切入。", "八一切入，及分別虛空一切入。", 2,
        [
            ("答：九行處為神通緣，除無色一切入。",
             "Đáp rằng: 9 hành xứ làm thần thông duyên, trừ vô sắc nhứt thiết nhập."),
            ("八一切入，及分別虛空一切入。",
             "Bát nhứt thiết nhập và phân biệt hư không nhứt thiết nhập."),
        ],
    )

    # 9. Q5 - Phẩm 8.2 (1682–1684)
    p = _replace_block(
        p, "S1_09_Q05_P08b_1682_1684",
        "入正受住者，成得第二禪，", "越人住故名為天住。", 3,
        [
            ("入正受住者，成得第二禪，離於二枝，成就二枝三種善十相具足。",
             "Nhập chánh thọ trụ nghĩa là thành được đệ nhị thiền, lìa nơi 2 chi. Thành tựu 2 chi, 3 loại thiện và 10 tướng cụ túc."),
            ("二十三功德相應，是天住是功德，生光耀天。如初廣說。",
             "Tương ưng với 23 công đức. Đây là trụ nơi công đức ở cõi Trời. Sanh vào Quang Diệu Thiên, như ở đầu đã nói rộng."),
            ("天住者，從定生喜樂，越人住故名為天住。",
             "Ở cõi trời là từ định sanh hỷ lạc; qua khỏi cõi của người ở nên gọi tên là chỗ ở của Trời."),
        ],
    )

    # 10. Q5 - Phẩm 8.2 (1703–1704)
    p = _replace_block(
        p, "S1_10_Q05_P08b_1703_1704",
        "已觀二禪過患，復見三禪功德，", "不久以無喜樂令心得安解三禪枝。", 2,
        [
            ("已觀二禪過患，復見三禪功德，是依一切入相作意，令喜心滅。",
             "Quán rồi nhị thiền quá hoạn. Lại thấy tam thiền công đức. Đây nương vào tất cả nhập tướng tác ý, làm cho tâm hỷ diệt."),
            ("以由喜樂受持心，如是作意，不久以無喜樂令心得安解三禪枝。",
             "Lấy mà do hỷ lạc thọ trì tâm, như thế tác ý. Chẳng chờ lấy vô hỷ lạc làm cho tâm được an ổn giải rõ nơi tam thiền chi."),
        ],
    )

    # 11. Q6 - Phẩm 8.3 (1940–1942)
    p = _replace_block(
        p, "S1_11_Q06_P08c_1940_1942",
        "越識處者，成越此識超入正度，", "入無所有處定心心數法，此謂無所有處。", 3,
        [
            ("越識處者，成越此識超入正度，此謂越一切識處。",
             "Kẻ qua khỏi thức xứ, thành qua khỏi thức nầy siêu nhập vào chánh độ. Đây nghĩa là vượt lên tất cả thức xứ."),
            ("無所有者，不復修行、不復分別、成失彼識、但見無所有，此謂無所有處。入無所有處定心心數法，此謂無所有處。",
             "Kẻ Vô sở hữu chẳng lại tu hành, chẳng lại phân biệt, thành mất thức kia, thường thấy vô sở hữu. Đây nghĩa là Vô sở hữu xứ."),
        ],
    )

    # 12–16. Q5 - Phẩm 8.2 (Hỏa, Phong [kèm 3B 2040-2041], Hoàng, Xích, Quang Minh)
    p = _replace_block(
        p, "S1_12_Q05_P08b_Hoa",
        "火相巧於放意為相，", "如地一切入所說功德。", 2,
        [
            ("火相巧於放意為相，不除火想為味，作意無雙為處。",
             "Tướng của lửa xảo; nên phóng ý là tướng. Chẳng trừ lửa tướng là vị. Tác ý vô song là xứ."),
            ("何功德者，不共五功德：於火一切入經營、起煙炎以光明想起、滅餘色光、隨意所燒、以作光明曉了於火界，如地一切入所說功德。",
             "Công đức gì vậy? Chẳng cùng với 5 công đức. Đối với hỏa nhứt thiết nhập kinh doanh, khởi lên ánh sáng và lấy ánh sáng đó làm tướng khởi. Mất ánh sáng rồi, tùy ý mà đốt. Lấy chỗ ánh sáng sớm rõ nơi hỏa giới. Như địa nhứt thiết nhập chỗ nói công đức."),
        ],
    )

    p = _replace_block(
        p, "S1_13_Q05_P08b_Phong_2040_2041",
        "放意為相，不除風想為味，", "如地一切入所說功德，修風一切入方便。", 3,
        [
            ("放意為相，不除風想為味，作意無雙為處。",
             "Lấy phóng ý làm tướng; chẳng trừ gió tưởng làm vị. Tác ý vô song làm xứ."),
            ("何功德者，不同三功德，於風一切入風行自在、能令風起、作意受持令清涼。",
             "Công đức như thế nào? - Chẳng giống 3 công đức. Đối với gió tất cả nhập, gió làm tự tại, có thể làm cho gió khởi; tác ý thọ trì làm cho mát mẻ."),
            ("如地一切入所說功德，修風一切入方便。",
             "Như địa nhập nhứt thiết chỗ nói công đức. Tu gió nhứt thiết nhập phương tiện."),
        ],
    )

    p = _replace_block(
        p, "S1_14_Q05_P08b_Hoang",
        "於黃一切入放意是相，", "修黃一切入處處皆見黃。", 2,
        [
            ("於黃一切入放意是相，不除黃想為味，作意無雙為處。",
             "Đối với hoàng nhứt thiết nhập phóng ý là tướng. Chẳng trừ hoàng tưởng là vị. Tác ý vô song là xứ."),
            ("何功德者，不同五功德，於黃一切入心隨逐得淨解脫，得黃除入作意，如金花種種黃色，修黃一切入處處皆見黃。",
             "Có công đức gì? - Chẳng đồng với 5 công đức. Đối với hoàng nhứt thiết nhập, tâm tùy toại được tịnh giải thoát, được màu vàng, trừ nhập tác ý. Như hoa màu vàng có nhiều loại màu vàng. Tu hoàng nhứt thiết nhập là nơi nơi đều thấy màu vàng."),
        ],
    )

    p = _replace_block(
        p, "S1_15_Q05_P08b_Xich",
        "於赤相放意為相，", "如說於地一切入。", 2,
        [
            ("於赤相放意為相，不離赤想為味，作意無二為處。",
             "Đối với tướng đỏ phóng ý làm tướng. Chẳng lìa đỏ tưởng làm vui. Tác ý vô nhị làm xứ."),
            ("何功德者，不共四功德，於赤一切入隨心得淨解脫，得赤除入，化種種赤色。不共功德者，如說於地一切入。",
             "Công đức như thế nào? - Chẳng cùng với 4 công đức. Đối với xích nhứt thiết nhập, tùy tâm được tịnh giải thoát, được xích trừ nhập; hóa ra nhiều loại màu đỏ chẳng cùng với công đức, như nói ở nơi địa nhứt thiết nhập."),
        ],
    )

    p = _replace_block(
        p, "S1_16_Q05_P08b_QuangMinh",
        "光明放意為相，", "修光明一切入處處見光明。", 2,
        [
            ("光明放意為相，不離光明想為味，作意無二為處。",
             "Ánh sáng phóng ý làm tướng. Chẳng lìa ánh sáng tưởng làm vị. Tác ý vô nhị làm xứ."),
            ("何功德者，與白功德等，修光明一切入處處見光明。",
             "Công đức gì? - Cùng với màu trắng công đức, tu quang minh nhứt thiết nhập; nơi nơi đều thấy ánh sáng."),
        ],
    )

    # 17–18. Q6 - Phẩm 8.3: 2 lỗi tách dấu hỏi CBETA
    p = _replace_block(p, "S1_17_Q06_CBETA_typo1", "何？", "處何功德？", 2, [("何處？", "xứ nào?"), ("何功德？", "công đức gì?")])
    p = _replace_block(p, "S1_18_Q06_CBETA_typo2", "何？", "味何處？", 2, [("何味？", "vị gì?"), ("何處？", "xứ gì?")])

    # 19–20. Q6 - Phẩm 8.3 (2545–2546, 2555–2556)
    p = _replace_block(
        p, "S1_19_Q06_P08c_2545_2546",
        "若人修行念戒成，得十二功德成，", "一切戒功德，是念戒功德。", 2,
        [
            ("若人修行念戒成，得十二功德成，尊重師、重法、重僧、重戒學、重供養、重不放逸、於細微過患常見憂怖、護自身亦護他、從此世怖畏解脫、彼世怖畏解脫、多歡喜可愛。",
             "Nếu người tu hành niệm giới, thành được 13 công đức. Thành được những việc như tôn trọng Sư trưởng, trọng giáo pháp, trọng Tăng, trọng học giới, trọng việc cúng dường và trọng việc chẳng buông lung. Đối với việc lo sợ nhỏ nhoi cũng thường hay thấy lo sợ: gìn giữ cho chính mình và cũng gìn giữ cho người khác nữa. Từ đời nầy lo sợ việc giải thoát, cho đến đời khác cũng lo ngại việc giải thoát. Nhiều hoan hỷ dễ thương."),
            ("一切戒功德，是念戒功德。",
             "Với tất cả công đức của giới. Đây có nghĩa là công đức của việc niệm giới."),
        ],
    )
    p = _replace_block(
        p, "S1_20_Q06_P08c_2555_2556",
        "以餘行當念戒。", "是姓可貴，以財物自在。", 2,
        [
            ("以餘行當念戒。", "Ngoài ra còn làm việc niệm giới."),
            ("名戒者，是樂無過患、是姓可貴，以財物自在。",
             "Nên gọi tên là giới. Đây là niềm vui chẳng lo sợ. Đây là tánh quý hóa; đây là tài vật tự tại."),
        ],
    )

    # 21. Q7 - Phẩm 8.4 (2762–2765)
    p = _replace_block(
        p, "S1_21_Q07_P08d_2762_2765",
        "何功德者，若修行念死，", "常觀世間心生厭患，此謂智相應念。", 4,
        [
            ("何功德者，若修行念死，於上善法成不放逸、成憎不善法，於諸服飾不多受畜、心不慳悋，見身壽命心不貪著，作無常想、苦想、無我想皆令成滿，成向善趣向於醍醐，臨命將終心不謬誤。",
             "Công đức nào? - Nghĩa là nếu người tu hành nhớ đến việc chết thì lấy pháp lành cao nhất thành chẳng phóng dật, trở thành ghét pháp chẳng lành. Lấy đồ phục sức chẳng nhiều để mặc, tâm chẳng keo kiệt. Thấy thọ mệnh của thân, tâm chẳng tham trước, liền nghĩ đến vô thường, nhớ đến khổ và vô ngã. Tất cả đều làm cho đầy đủ, thành ra hướng đến cõi lành, hướng đến chỗ yên ổn. Khi lâm chung, tâm chẳng lầm lẫn."),
            ("云何修行？初坐禪人入寂寂坐，攝一切心，以不亂心念眾生死，我入死法、向於死趣、不過死法，如涅底履波陀脩多羅中說。若人樂觀死，當觀被殺人見死因緣。於是念死有四種：憂相應、驚相應、中人相應、智相應。",
             "Vì sao người tu hành mới tọa thiền nhập vào tịch tĩnh? Vì ngồi nhiếp tất cả tâm, lấy tâm bất loạn nhớ đến sự chết của chúng sanh. Ta vào trong pháp chết, hướng đến cõi chết; chẳng sợ pháp chết; giống như trong kinh Niết Đề Phúc Ba Đà đã nói: Nếu có người vui quán về sự chết thì hãy nên quán về kẻ bị giết và thấy nhơn duyên của sự chết, mà đối với niệm tử nầy có 4 loại. Tương ưng với lo, tương ưng với sợ, tương ưng với người khác và tương ưng với trí."),
            ("如喪愛子心生緣念，此謂憂相應；悲念童子卒暴命終，此謂驚相應念；如闍維人念離生故，此謂中相應念；常觀世間心生厭患，此謂智相應念。",
             "Như có tâm yêu mến con, tâm sanh duyên niệm. Đây gọi là tương ưng với lo. Thương nhớ con mình đã sớm mệnh chung. Đây gọi là niệm tương ưng với sự sợ hãi. Như người bị thiêu nhớ đến sự lìa sự sống vậy. Đây gọi là niệm tương ưng với người khác. Thường quan sát thế gian tâm sanh lo sợ. Đây gọi là niệm tương ưng của trí."),
        ],
    )

    # 22–23. Q8 - Phẩm 8.5 (3085–3088, 3393–3394)
    p = _replace_block(
        p, "S1_22_Q08_P08e1_3085_3088",
        "何起者，是根令起。", "何事者，於眾生為事。", 4,
        [
            ("何起者，是根令起。", "Khởi lên cái gì? - Căn nầy làm cho khởi."),
            ("何具足者，若慈成就，殺除瞋恚、除不善愛，令身口意業清淨，此謂具足。",
             "Đầy đủ thế nào? Nếu lòng từ thành tựu, giết trừ sân nhuế, trừ đi cái yêu thương chẳng lành, làm cho thân, miệng, ý nghiệp được thanh tịnh. Đây gọi là đầy đủ."),
            ("何非具足者，以二因失慈：以自朋生怨，以不善愛；以對治生怨，以起瞋恚，此謂非具足。",
             "Những gì là không đầy đủ? Dùng 2 nguyên nhân mất đi lòng từ; lấy chính người quen của mình rồi sanh oán, dùng cái ái không thuận; lấy sự đối trị sanh oán, lấy việc ấy khởi lên sân nhuế. Đây nghĩa là không đầy đủ."),
            ("何事者，於眾生為事。", "Việc gì? - Đối với tất cả chúng sanh là công việc vậy."),
        ],
    )
    p = _replace_block(
        p, "S1_23_Q08_P08e2_3393_3394",
        "問：云何於食不耐想？何修？", "何相？", 2,
        [
            ("問：云何於食不耐想？", "Hỏi rằng: Vì sao đối với việc ăn uống chẳng thể chịu theo tưởng?"),
            ("何修？何相？", "Tu cái gì, tướng gì?"),
        ],
    )

    # 24–25. Q9 - Phẩm 9 (3575–3577, 3626–3627)
    p = _replace_block(
        p, "S1_24_Q09_P09_3575_3577",
        "初坐禪人遠螺鼓等聲，", "不應作意於最可畏。", 3,
        [
            ("初坐禪人遠螺鼓等聲，彼聲依自性耳，以天耳智應作意於聲相，令起天耳智。",
             "Người mới tọa thiền nghe được tiếng xa xa của ốc tù-và và tiếng trống v.v... Âm thanh kia nương vào nơi tự tánh của lỗ tai. Dùng thiên nhĩ trí nên tác ý với tướng của âm thanh. Làm cho khởi lên thiên nhĩ trí."),
            ("或細聲或大聲、或遠聲或近聲，唯天耳應取。",
             "Hoặc âm thanh nhỏ; hoặc âm thanh lớn; hoặc âm thanh xa; hoặc âm thanh gần. Chỉ có thiên nhĩ mới thuận tai."),
            ("於是初坐禪人，不應作意於最可畏。",
             "Đối với kẻ sơ thiền chẳng nên tác ý đối với việc quá sợ."),
        ],
    )
    p = _replace_block(
        p, "S1_25_Q09_P09_3626_3627",
        "答：光明為九、或光明為五、", "業果報所成、修行所成。", 2,
        [
            ("答：光明為九、或光明為五、或光明一切入事，於第四禪得自在，有眼性是其所能起。",
             "Đáp rằng: Ánh sáng ấy có 9 thứ. Hoặc ánh sáng ấy có 5; hoặc ánh sáng ấy gồm tất cả mọi việc. Đối với đệ tứ thiền được tự tại có được nhãn tánh thì từ đây có thể khởi lên được."),
            ("幾種天眼者，答二種天眼，業果報所成、修行所成。",
             "Có bao nhiêu loại thiên nhãn? Đáp rằng: Có 2 loại thiên nhãn do nghiệp quả báo mà thành hoặc do tu hành mà thành."),
        ],
    )

    # 26. Q11 - Phẩm 11.2 (4346–4349)
    p = _replace_block(
        p, "S1_26_Q11_P11b_4346_4349",
        "問：云何？世諦果苦，集世諦因，", "此四聖諦，以十一行可勝可知。", 4,
        [
            ("問：云何？世諦果苦，集世諦因，果滅，出世諦果。",
             "Hỏi: Những gì là Thế Đế quả, khổ tập thế đế nhơn quả? Đáp: Diệt xuất Thế Đế quả."),
            ("道，出世諦因。是故四，不三不五。",
             "Đạo xuất Thế Đế nhơn, rồi duyên vào nhau mà làm 4. Chứ chẳng phải 3 hay 5."),
            ("復次應知、應斷、應證、應修，以四句故成四。",
             "Lại nữa nên biết, nên đoạn, nên chứng, nên tu. Dùng 4 câu ấy nên trở thành 4."),
            ("此四聖諦，以十一行可勝可知。",
             "Đây là Tứ Thánh Đế lấy 11 hành có thể khá biết rõ hơn."),
        ],
    )

    # 27–30. Q12 - Phẩm 12.2 (4893–4901, 4922–4928, 4935–4947, 4954–4961)
    p = _replace_block(
        p, "S1_27_Q12_4893_4901",
        "爾時人來，為日所曝，熱乏渴愛。", "二緣為起：作意一切相，及無相界不作意。", 9,
        [
            ("爾時人來，為日所曝，熱乏渴愛。彼人見井知有水，彼不以身觸住。如是我長老有滅為泥洹，如實正智善見，我非阿羅漢漏盡。",
             "Lúc ấy có người đến và trời nóng nên khát nước, người kia thấy giếng, biết là có nước mà kẻ kia chẳng dùng tự thân của mình để tự biết, như thế Trưởng Lão có diệt Niết Bàn, như thật chánh trí thiện kiến. Ta chẳng phải A La Hán lậu tận."),
            ("何故令起者，答：為現見法樂住令起。如世尊教阿難，是時阿難如來不作意，一切諸相唯一受滅，無相心定令起住，是時阿難如來身成安隱。",
             "Vì sao mà làm cho khởi lên được? Đáp: Vì hiện thấy pháp lạc trú nên khởi, như Đức Thế Tôn đã dạy Ngài A Nan: Lúc ấy Ngài A Nan đối với Đức Như Lai không tác ý về tất cả các tướng, duy chỉ có một thọ diệt, tâm vô tướng định làm cho khởi lên trụ. Lúc ấy Ngài A Nan thành thân Như Lai an ổn."),
            ("云何以令起者，答：彼坐禪人入寂寂住，或住或臥，樂得果正受。作生滅見所初觀諸行，乃至性除智，性除智無間於泥洹果正受令安，依其禪成修道是。",
             "Và vì sao mà làm cho khởi lên? Đáp: Kẻ tọa thiền kia nhập vào sự tịch tịnh rồi đứng, hoặc ngồi, hoặc nằm vui với quả chánh thọ vừa được; tạo ra sự sanh diệt nơi chỗ thấy. Đầu tiên quán về các hành cho đến tánh trừ trí. Tánh trừ trí không gián đoạn. Đối với quả Niết Bàn làm cho an ổn. Nương vào nơi thiền nầy thành con đường để tu vậy."),
            ("是禪成所作，是名果正受。",
             "Thiền nầy thành chỗ tạo tác. Đây nghĩa là quả chánh thọ."),
            ("云何作意者，答：無為醍醐界以寂作意。",
             "Thế nào là tác ý? Đáp: Vô vi đề hồ giới lấy sự yên lặng mà tác ý."),
            ("彼成就幾緣？幾緣為住？幾緣為起？",
             "Cái kia sẽ thành tựu bao nhiêu duyên; bao nhiêu duyên trụ; bao nhiêu duyên để khởi?"),
            ("答：彼正受二緣，不作意一切諸相，於無相界作意。",
             "Đáp: Chánh thọ kia có 2 duyên. Đó là bất tác ý tất cả các tướng và đối với vô tướng giới tác ý."),
            ("三緣為住：不作意一切諸相，於無相界作意，及初行。",
             "Ba duyên để trụ gồm bất tác ý tất cả các tướng; đối với vô tướng giới tác ý và sơ hành."),
            ("二緣為起：作意一切相，及無相界不作意。",
             "2 duyên cùng khởi: Tác ý tất cả tướng và vô tướng giới bất tác ý."),
        ],
    )

    p = _replace_block(
        p, "S1_28_Q12_4922_4928",
        "答：不生心心數法，此謂滅想受定。", "以奢摩他力、以毘婆舍那力。", 7,
        [
            ("答：不生心心數法，此謂滅想受定。",
             "Đáp: Chẳng sanh tâm, tâm số pháp. Đây nghĩa là diệt tưởng thọ định."),
            ("誰令起定者，答：阿羅漢及阿那含，於此定作滿。",
             "Ai đã làm cho khởi định nầy? Đáp: A La Hán và A Na Hàm. Đối với định nầy đã đầy đủ."),
            ("誰不令起者，答：凡夫人及須陀洹、斯陀含，及生無色界人，於是非其境界故。",
             "Ai chẳng khởi lên? Đáp: Kẻ phàm phu và Tu Đà Hoàn, Tư Đà Hàm và người sanh ở cõi vô sắc giới. Đối với đây chẳng phải là cảnh giới vậy."),
            ("凡夫不能起煩惱障礙定，未斷故。",
             "Kẻ phàm phu chẳng nên khởi phiền não, chướng ngại định, vì chưa đoạn vậy."),
            ("須陀洹、斯陀含不能起，為更起。",
             "Tu Đà Hoàn, Tư Đà Hàm chưa nên khởi thì liền làm cho khởi lên."),
            ("非其處故，入無色界不能起。",
             "Chẳng phải là chỗ nầy vậy, nhập vô sắc giới chẳng nên khởi."),
            ("幾力成就令起者，答：以二力成就令起，以奢摩他力、以毘婆舍那力。",
             "Có bao nhiêu lực thành tựu làm cho khởi? Đáp: Lấy 2 lực thành tựu làm cho khởi. Đó là Xa Ma Tha lực và Tỳ Bà Xá Na lực."),
        ],
    )

    p = _replace_block(
        p, "S1_29_Q12_4935_4947",
        "於是入二禪覺觀，口行成所除；", "如長老舍利弗、如長老白鷺子底沙。", 13,
        [
            ("於是入二禪覺觀，口行成所除；入第四禪出息入息，身行成所除；入滅想受定人，想受心行成所除。",
             "Đối với đây nhập nhị thiền, giác quán khẩu hạnh, thành sở trừ. Nhập đệ tứ thiền hơi thở vào ra là thân hành, thành sở trừ. Người nhập diệt tưởng thọ định thì tưởng thọ tâm hành thành sở trừ."),
            ("初幾事者，答：初四事，一縛、不亂、遠分別、觀事非事。",
             "Đầu tiên có bao nhiêu việc? Đáp: Đầu tiên có 4 việc. Sự trói buộc chẳng loạn, xa phân biệt, quán sự phi sự."),
            ("於是名一縛者，鉢袈裟一處[怡-台+(噗-口)]受持。",
             "Đây tên là một sự trói buộc. Bát, Cà Sa một xứ, mang theo."),
            ("不亂者，以所有方便，此身願莫生亂受持。",
             "Chẳng loạn. Đây là phương tiện sở hữu. Thân nầy nguyện chưa sanh loạn thọ trì."),
            ("遠分別者，稱其身力，以日作分別受持，於此久遠過期當起。",
             "Viễn phân biệt là xưng tụng thân lực nầy. Dùng số ngày để phân biệt thọ trì. Đối với thời kỳ xa xôi sẽ khởi lên."),
            ("觀事非事者，未至時分別。或眾僧為事和合，以彼聲我當起受持。",
             "Quán sự phi sự nghĩa là chưa tới thời để phân biệt; hoặc chúng tăng vì sự hòa hợp dùng tiếng kia, ta sẽ khởi thọ trì."),
            ("於是一縛者，為守護袈裟。",
             "Nơi một sự trói buộc nầy, vì giữ gìn Cà Sa."),
            ("不亂者及久遠分別，為守護身。",
             "Nên chẳng loạn và phân biệt xa xôi, vì bảo hộ thân."),
            ("觀事非事者，為不妨眾僧和合，住無所有處，或初作事入初禪。",
             "Quán sự phi sự là vì không phường chúng tăng hòa hợp, trụ vô sở hữu xứ; hoặc sơ tác nhập sơ thiền."),
            ("何故令起？", "Vì sao lại làm cho khởi?"),
            ("答：為現法樂住者，是聖人最後無動定。復為起神通入廣定。",
             "Đáp: Vì hiện pháp lạc trú vậy. Đó là Thánh nhơn tối hậu vô động định, lại vì khởi thần thông nhập vào quảng định."),
            ("如長老正命羅漢，為守護身。如長老舍利弗、如長老白鷺子底沙。",
             "Như Trưởng Lão chánh mệnh A La Hán. Vì bảo hộ thân như Trưởng Lão Xá Lợi Phất, như Trưởng Lão Bạch Lộ Tử Đề Sa."),
        ],
    )

    p = _replace_block(
        p, "S1_30_Q12_4954_4961",
        "云何心以起者，若阿那含人以阿那含果心起，", "云何此定有為無為者，答：不可說此定有為無為。", 8,
        [
            ("云何心以起者，若阿那含人以阿那含果心起，若阿羅漢人以阿羅漢心起。",
             "Vì sao tâm lại khởi? Nếu người A Na Hàm thì dùng A Na Hàm quả để tâm khởi. Nếu người A La Hán thì dùng tâm A La Hán để khởi."),
            ("起已彼心何所著？", "Khởi rồi tâm kia dính mắc vào cái gì?"),
            ("答：心專緣寂寂。", "Đáp: Tâm chuyên duyên vào sự tịch tịnh."),
            ("幾觸所觸者，答：三觸所觸，以空觸、無相觸、無作觸。",
             "Có bao nhiêu xúc sở xúc? Đáp: Có 3 loại xúc sở xúc. Dùng không xúc, vô tướng và vô tác xúc."),
            ("云何初起諸行？彼從身行、從彼口行。",
             "Vì sao sở khởi các hạnh? Từ kia thân làm, từ kia khẩu làm."),
            ("死人及入滅想定人何差別者，死人，三行沒無現，壽命斷、煖斷、諸根斷。",
             "Người chết và người nhập diệt tưởng định có gì sai biệt? Kẻ chết thì 3 việc kia mất không còn gì nữa nơi mạng sống; đoạn hơi ấm, đoạn các căn và đoạn nhập."),
            ("入受想定人，三行斷沒，壽命不斷、煖不斷、諸根不異。",
             "Người thọ tưởng định 3 việc làm ấy đoạn; nhưng thọ mệnh không mất; hơi ấm chẳng mất, các căn không khác."),
            ("此彼差別。", "Chính đây là sự sai biệt."),
            ("云何此定有為無為者，答：不可說此定有為無為。",
             "Vì sao định nầy hữu vi và vô vi? Đáp: Khó thể nói đây là định hữu vi hay vô vi."),
        ],
    )
    return p


def _apply_stage2_clusters10(p: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Tầng 2: 9 cụm trượt chéo nhiều dòng còn lại (C2 đã gộp xử lý trọn vẹn ở S1_06_C2)."""
    # C1 (795–796): Bản Việt gốc bỏ sót '四聖道定，是為滅不為起。' -> gộp gọn 2 câu Hán để không lệch nghĩa
    p = _replace_block(
        p, "C1_Q02_P04_795_796",
        "答：欲界善不善定，此謂為起不為滅。", "四聖道定，是為滅不為起。", 2,
        [
            ("答：欲界善不善定，此謂為起不為滅。四聖道定，是為滅不為起。",
             "Đáp rằng: Dục giới thiện bất thiện định. Đây có nghĩa là khởi mà chẳng khởi."),
        ],
    )

    # C3 (2281–2284): Trượt 4 dòng Thực Đạm Tưởng
    p = _replace_block(
        p, "C3_Q06_P08c_2281_2284",
        "答：食噉者，或烏鵲鵄梟雕鷲、", "作意不淨為處，等膖脹想功德。", 4,
        [
            ("答：食噉者，或烏鵲鵄梟雕鷲、猪狗狐狼虎豹食噉死屍，此謂食噉。",
             "Đáp rằng: Việc ăn là do chim ưng, chim kênh kênh, chim thứu, giả can, chó sói, chồn, hổ, beo ăn tử thi ấy. Đây nghĩa là ăn xác chết."),
            ("於彼食噉是相。以正智知，此謂食噉想。",
             "Đối với sự ăn kia; tướng nầy lấy chánh trí mà biết. Đây nghĩa là tưởng về ăn."),
            ("心住不亂此謂修，食噉想為相，厭為味，作意不淨為處，等膖脹想功德。",
             "Tâm trụ bất loạn nghĩa là tu. Lấy tưởng ăn xác chết làm tướng. Xa lìa làm vị. Tác ý bất tịnh làm xứ và tưởng sình trướng là công đức."),
        ],
    )

    # C4 (2402–2406): Trượt 5 dòng Thế Gian Giải
    p = _replace_block(
        p, "C4_Q06_P08c_2402_2406",
        "世間解者，世間有二種，", "世尊悉知世間諸行，此謂世間解。", 5,
        [
            ("世間解者，世間有二種，謂眾生世間、行世間。",
             "Thế Gian Giải nghĩa là Thế Gian có 2 loại. Nghĩa là chúng sanh thế gian và hạnh thế gian."),
            ("世尊以一切行，知眾生世間，以知眾生種種欲樂。",
             "Đức Thế Tôn dùng tất cả hạnh biết chúng sanh trong thế gian, biết được tất cả nhiều loại dục lạc của chúng sanh."),
            ("以根差別，以宿命、以天眼、以從去來、以和合、以成就、以種種可化、以種種堪不堪、以種種生、以種種趣、以種種地、以種種業、以種種煩惱、以種種果報、以種種善惡、以種種縛解，以如是等行，世尊悉知眾生世間。",
             "Dùng căn sai biệt, dùng túc mệnh, thiên nhãn, từ quá khứ đến, lấy sự hòa hợp mà thành tựu. Dùng nhiều loại có thể giáo hóa, dùng nhiều loại sâu xa hoặc chẳng sâu, dùng những loại sanh, dùng những cõi, những đất để trồng các loại nghiệp, dùng các loại phiền não, lấy nhiều loại quả báo; lấy nhiều loại thiện ác, dùng nhiều loại trói, mở. Như thế các việc làm mà Đức Thế Tôn đều biết chúng sanh trong thế gian."),
            ("復說行世間者，世尊亦知。以一切業，亦知諸行，以定相、以隨其自相因緣、善不善無記、以種種陰、以種種界、以種種入、以智明了、以無常苦無我、以生不生，如是等行，世尊悉知世間諸行，此謂世間解。",
             "Lại nói Hành Thế Gian nghĩa là Đức Thế Tôn lại cũng biết tất cả nghiệp về thiện, bất thiện, vô ký. Lấy những loại ấm, lấy các giới, lấy các nhập, dùng trí tuệ để rõ biết. Lấy vô thường, khổ, vô ngã; lấy sanh chẳng sanh, như thế những việc làm Đức Thế Tôn đều biết những việc làm ở thế gian. Đây gọi là Thế Gian giải."),
        ],
    )

    # C5 (3281–3284): Trượt 4 dòng Quán Tứ Đại
    p = _replace_block(
        p, "C5_Q08_P08e2_3281_3284",
        "有大非實義令現實義，是故名大。", "如是大生，是故名大。", 4,
        [
            ("有大非實義令現實義，是故名大。",
             "Có đại chẳng phải thật nghĩa, làm cho hiện ra thật nghĩa. Nên đây gọi là đại."),
            ("大者，鬼等形名大。",
             "Đại là hồn so với hình hài; nên gọi là đại."),
            ("云何大生名大？諸界大生。",
             "Các giới đại sanh ra."),
            ("如世尊所說偈：略說地相， 有二十萬， 四那由他；水四十萬， 八那由他； 風住虛空，乃九十萬， 六那由他； 世界所住，亦以火成， 世界之中， 有諸光焰，上至梵世， 乃極七日。如是大生，是故名大。",
             "Như thế Đức Thế Tôn nói kệ rằng: Lược nói tướng đất Có hai mươi vạn Bốn Na Do Tha Nước bốn mươi vạn Tám Na Do Tha Gió trụ hư không Đến chín mươi vạn Sáu Na Do Tha Thế giới chỗ trụ Lại do lửa thành Ở trong thế giới Có các ánh sáng Trên đến Phạm Thế Cho đến bảy ngày Như thế đất sanh Cho nên tên đại."),
        ],
    )

    # C6 (3773–3777): Trượt chéo 5 dòng Thân / Sắc / Thanh / Hương / Vị nhập
    p = _replace_block(
        p, "C6_Q10_P11a_3773_3777",
        "復次除毛髮爪齒，所餘不受。", "是有對味，此謂味入。", 5,
        [
            ("復次除毛髮爪齒，所餘不受。於一切受身，初業所造、地大最多，四大所造清淨色，此謂身入。",
             "Lại nữa trừ lông, tóc, móng tay, răng là chỗ chẳng thọ; nhưng với tất cả đều thọ giữ và do chỗ nghiệp đầu tiên tạo tác mà đất là chỗ nhiều nhất. Do tứ đại là chỗ tạo ra màu sắc thanh tịnh. Đây gọi là thân nhập."),
            ("是可見色，此謂色入。", "Điều có thể thấy màu sắc gọi là sắc nhập."),
            ("是有對聲，是謂聲入。", "Đối với âm thanh thì có thinh nhập."),
            ("是有對香，此謂香入。", "Đối với mùi thì có hương nhập."),
            ("是有對味，此謂味入。", "Đối với vị thì có vị nhập."),
        ],
    )

    # C7 (3842–3853): Chuỗi trượt dài nhất 12 dòng liên tiếp (Nhập thai & Hóa sanh)
    p = _replace_block(
        p, "C7_Q10_P11a_3842_3853",
        "答：如男女入胎，於剎那生三十色起，", "如是以生可知。", 12,
        [
            ("答：如男女入胎，於剎那生三十色起，所謂處十、身十、或女根十或男根十。",
             "Đáp rằng: Như nam nữ nhập thai, chỉ trong sát na 30 sắc ở nơi 10 xứ, thân 10 hoặc nữ căn 10; hoặc nam căn 10."),
            ("不男不女二十色起，所謂處十、身十。",
             "Chẳng phải nam chẳng phải nữ có 20 sắc khởi lên. Cho nên xứ có 10 và thân có 10."),
            ("於欲界化生，滿根入男女，於生剎那七十色起，所謂處十、身十、眼十、耳十、鼻十、舌十、或女根十或男根十。",
             "Đối với dục giới hóa sanh đầy đủ căn của nam nữ nhập vào, chỉ trong sát na sanh ra 70 sắc; nên có 10 xứ, thân 10, mắt 10, tai 10, mũi 10, lưỡi 10; hoặc nữ căn 10, hoặc nam căn 10."),
            ("或於惡趣化生生盲女人男人，於其生剎那六十色起，除眼十。如是生聾人六十色起，除耳十。",
             "Hoặc đối với cõi ác thú hóa sanh thì sanh ra đui mù và người nam người nữ ấy trong sát na sanh ra 60 sắc ngoại trừ nhãn 10. Như thế sanh ra người điếc và 60 sắc khởi lên, ngoại trừ nhĩ có 10."),
            ("生盲聾人五十色起，除眼十、耳十。",
             "Người sinh ra mù, điếc có 50 sắc khởi lên, ngoại trừ nhãn 10 và nhĩ 10."),
            ("惡趣化生滿根入，或非男或非女。及劫初人，於其生剎那六十色起，除男女根。",
             "Từ ác thú hóa sanh đầy đủ căn nhập vào hoặc phi nam phi nữ và người ở kiếp đầu, chỉ trong sát na khởi lên 60 sắc trừ căn của nam nữ."),
            ("於彼盲及非男非女，五十色起，除眼根十、除非男非女根。",
             "Với kẻ mù và phi nam phi nữ kia có 50 sắc khởi lên, trừ nhãn căn 10 và trừ phi nam phi nữ căn."),
            ("或聾非男非女，亦五十色起，除耳十及非男非女根。",
             "Hoặc điếc phi nam phi nữ lại có 50 sắc khởi lên, ngoại trừ tai 10 và phi nam phi nữ căn."),
            ("或盲聾非男非女，四十色起，處十、身十、鼻十、舌十。",
             "Hoặc mù điếc, phi nam phi nữ có 40 sắc khởi: xứ 10, thân 10, mũi 10, lưỡi 10."),
            ("梵天於其生剎那，四十九色起，處十、眼十、耳十、身十、命根九。",
             "Phạm Thiên đối với đây trong sát na sanh ra 49 sắc khởi: xứ 10, mắt 10, tai 10, thân 10, mệnh căn 9."),
            ("無想天眾生於其生剎那，九色起，命根九。",
             "Vô Tưởng Thiên chúng sanh đối với sự sanh nầy trong sát na có 9 sắc khởi lên: mệnh căn có 9."),
            ("如是以生可知。", "Như thế lấy sự sanh mà biết."),
        ],
    )

    # C8 (4381–4384): Trượt chéo 4 dòng Tứ Đế thí dụ
    p = _replace_block(
        p, "C8_Q11_P11b_4381_4384",
        "如此岸有苦有怖畏，如是苦可知。", "如船能渡，如是道可知。", 4,
        [
            ("如此岸有苦有怖畏，如是苦可知。",
             "Như ở bờ nầy có khổ, có sợ hãi; khổ như thế, nên rõ biết."),
            ("如流，如是集可知。",
             "Như lưu chảy, chính là tập, nên rõ biết."),
            ("如彼岸無苦無怖畏，如是滅可知。",
             "Như ở bờ kia không khổ, không sợ hãi. Như vậy là diệt, nên rõ biết."),
            ("如船能渡，如是道可知。",
             "Như thuyền bè có thể chở người qua. Như thế chính là đạo, nên rõ biết."),
        ],
    )

    # C9 (4471–4475): Trượt 5 dòng Phân biệt Khổ Tập Diệt
    p = _replace_block(
        p, "C9_Q11_P12a_4471_4475",
        "如是無明緣行，行緣識，生緣老死，", "為苦滅。誰滅？", 5,
        [
            ("如是無明緣行，行緣識，生緣老死，成憂悲苦惱，如是悉苦陰成起。",
             "Như vậy vô minh duyên vào hành, hành duyên vào thức, sanh duyên vào lão tử, trở thành ưu bi khổ não. Như vậy tất do khổ ấm khởi lên."),
            ("彼坐禪人如是以因緣所縛以廣觀，爾時以作略，此受緣愛，彼苦集令起。",
             "Kẻ tọa thiền kia, đây là do nhơn duyên trói buộc, phải quán rộng ra. Bấy giờ chỉ nói lược: thọ nầy duyên vào ái và khổ, tập kia làm cho khởi lên."),
            ("或法住智、或聖取因緣智，或離疑清淨，此眾語言集諦令起智。",
             "Hoặc pháp trụ trí; hoặc thanh thủ nhân duyên trí; hoặc lìa nghi thanh tịnh. Những lời nói nầy tập đế làm cho khởi lên trí."),
            ("彼坐禪人以令起苦集，於三昧已度疑，爾時觀苦滅，誰滅？",
             "Kẻ tọa thiền kia làm cho khởi lên sự khổ tập. Đối với 3 thời gian trải qua chỗ nghi. Lúc ấy quán về khổ diệt là ai diệt?"),
            ("為苦滅。誰滅？", "Khổ diệt là ai?"),
        ],
    )

    # C10 (4654–4665): Chuỗi trượt chéo 12 dòng Thí dụ Thuyền & Mặt Trời
    p = _replace_block(
        p, "C10_Q12_P12b_4654_4665",
        "如譬喻偈所說：如人捨此岸，", "如日，如是聖智。", 12,
        [
            ("如譬喻偈所說：如人捨此岸， 以船度彼岸，於彼度諸物， 乘舡者除漏。",
             "Như người bỏ bờ nầy Dùng thuyền qua bờ kia Nơi bờ kia các vật Kẻ lên thuyền quên đi."),
            ("如船度水，非初非後於一剎那作四事，捨此岸、除漏、到彼岸、度物。",
             "Như thuyền trên nước, chẳng đầu chẳng cuối. Đối với trong mỗi sát na tạo ra 4 việc. Bỏ bờ nầy, trừ lậu, qua đến bờ kia, vật qua đó."),
            ("如捨此岸，如是智分別苦。",
             "Như bỏ bờ nầy, như vậy trí phân biệt khổ."),
            ("如除漏，如是分別斷集。",
             "Giống như trừ hữu lậu, như vậy sự phân biệt đoạn tập."),
            ("如度彼岸，如是作證分別滅。",
             "Cũng giống qua bờ bên kia, như vậy sự tác chứng phân biệt."),
            ("如以船度物，如是修道分別。",
             "Lại như dùng thuyền để độ vật, như thế tu đạo phân biệt."),
            ("如燈共生，於一剎那不初不後作四事，如小燈炷、除闇、令油消、令光明起。",
             "Như đèn cùng sáng. Đối mỗi sát na chẳng đầu chẳng cuối tạo ra 4 việc. Như ánh sáng nhỏ trừ sự tối tăm, làm cho dầu tiêu hao và làm cho ánh sáng khởi lên."),
            ("如日共生，非初非後於一剎那作四事，令現色、除闇、令滅寒、令起光明。",
             "Như mặt trời sáng, không có đầu, không có cuối. Đối với từng sát na tạo ra 4 việc, làm cho hiện sắc để trừ ám, làm cho hết lạnh, làm cho khởi lên ánh sáng."),
            ("如令現色，如是智分別苦。",
             "Như làm cho hiện sắc. Như thế trí phân biệt khổ ấy."),
            ("如除闇，如是分別斷集。",
             "Như trừ sự tối tăm, như vậy sự phân biệt đoạn tập."),
            ("如令滅寒，如是作證分別滅。",
             "Như làm cho mất đi sự lạnh, như thế sự túc chứng phân biệt diệt."),
            ("如令起光明，如是修道分別。如日，如是聖智。",
             "Như làm cho khởi lên ánh sáng, như vậy sự tu đạo phân biệt giống như mặt trời, như là Thánh trí."),
        ],
    )
    return p


def _apply_stage3_3a_3b(p: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Tầng 3: Toàn bộ 45 cặp 3A (此謂X/是名X) và 19 cặp 3B còn lại (2040-2041 đã sửa tại S1_13)."""
    # --- NHÓM 3A: Q1–Q2 ---
    p = _replace_block(
        p, "3A_232_233",
        "以二因緣戒成清淨：", "二犯不悔，此謂不清淨。", 2,
        [
            ("以二因緣戒成清淨：一不犯、二犯已能悔，此謂清淨戒。",
             "Lấy hai nhơn duyên giới, thành thanh tịnh. Một là chẳng phạm và hai là phạm rồi sau đó hối quá. Đây gọi là giới thanh tịnh."),
            ("以二因緣成不清淨：一自故犯、二犯不悔，此謂不清淨。",
             "Lấy 2 nhơn duyên thành bất tịnh giới. Một là tự cố phạm; hai là phạm mà chẳng hối quá. Đây gọi là bất tịnh giới."),
        ],
    )
    p = _replace_block(
        p, "3A_356_357",
        "答：於見聞覺知色聲香味觸法煩惱相著，", "於守護根人和合故。", 2,
        [
            ("答：於見聞覺知色聲香味觸法煩惱相著，及受持不犯，此謂守護根威儀戒。",
             "Đáp rằng: Đối với việc thấy nghe đều rõ biết sắc thanh hương vị xúc pháp, là do đắm trước tướng phiền não và lãnh giữ chẳng phạm. Đây gọi là giới giữ gìn các căn uy."),
            ("此守護根戒，以九行成滿：以惡為相斷諸根故、彼對治不作意故、如救頭然終不暫捨故、如見難陀以威儀故、伏惡心故、於定相心自在故、不守護根人遠離故、於守護根人和合故。",
             "Đây là thủ hộ căn giới lấy 9 việc làm được thành tựu đầy đủ. Lấy ác làm tướng, đoạn các căn vậy. Đối trị kia không tác ý nên như cứu đầu cháy, chung cuộc chẳng dần xả bỏ. Như thấy Nan Đà, lấy uy nghi mà phục tâm ác vậy. Đối với tâm tưởng định, được tự tại chăng? Người giữ gìn các căn thì xa lìa vậy. Đối với người giữ gìn các căn hòa hợp vậy."),
        ],
    )
    p = _replace_block(
        p, "3A_375_378",
        "答：不為兇險行、不為自高、", "此謂少功德觀。", 4,
        [
            ("答：不為兇險行、不為自高、不為先身、不為嚴首，此謂可斷觀。",
             "Đáp rằng: Chẳng làm việc hung hiểm, chẳng tự cao, chẳng vì thân mình trước, chẳng làm việc nghiêm thủ. Đây nghĩa là khả đoạn quán."),
            ("為此身住、為正調護、為除飢渴、為攝受梵行，此謂事觀。",
             "Vì thân nầy trụ, vì chánh điều hộ, vì trừ đói khát, vì nhiếp thọ phạm hạnh. Sự quán."),
            ("我當除先病不起新疾者，此謂以少自安觀。",
             "Nghĩa là ta sẽ trừ bịnh là điều đầu tiên mà chẳng khởi lên tật mới. Đây gọi là lấy ít quán tự an."),
            ("我當以少自安無過成安樂住，此謂少功德觀。",
             "Nghĩa là ta lấy ít tự an, chẳng quá, thành ở chỗ an lạc. Đây là lấy ít quán công đức."),
        ],
    )
    p = _replace_block(
        p, "3A_483_484",
        "或於塚間、或於糞掃、或於市肆、", "此謂世人所棄。", 2,
        [
            ("或於塚間、或於糞掃、或於市肆、或於道路，拾剪浣染掩緝裁縫，成就受持，此謂無主。",
             "Hoặc ở nơi gò mả cao; hoặc ở nơi phấn tảo; hoặc ở nơi thị tứ; hoặc ở nơi đường sá, nhặt được rồi góp lại nhuộm đi rồi chắp vá thành hình mới thọ nhận. Đây nghĩa là vô chủ."),
            ("或剪鑿之餘，牛鼠所嚙、或火所燒、或人所擲，施覆尸衣及外道服，此謂世人所棄。",
             "Phẩn nhạt như phân bò; hoặc chỗ hỏa thiêu; hoặc người bỏ đi, cho y che nhà và áo ngoại đạo. Đây gọi là đồ bỏ của người đời."),
        ],
    )
    p = _replace_block(
        p, "3A_746_747",
        "不善一心，是謂邪定；", "邪定當斷，正定應修。", 2,
        [
            ("不善一心，是謂邪定；若善一心，是謂正定。",
             "Chẳng lành nhứt tâm. Đây nghĩa là tà định. Nếu lành một tâm. Đây nghĩa là chánh định."),
            ("邪定當斷，正定應修。", "Tà định dứt mất, chánh định nên tu."),
        ],
    )

    # --- NHÓM 3A: Q3–Q4 ---
    p = _replace_block(
        p, "3A_959_960",
        "答：欲行人五煩惱，多行嫉、", "多行忿、恨、覆、慳、瞋，此謂五。", 2,
        [
            ("答：欲行人五煩惱，多行嫉、慳、幻、諂、欲，此謂五。",
             "Đáp rằng: Dục hành nhơn có 5 phiền não. Đó là đa hành, keo kiệt, huyễn, siểm, dục. Đây nghĩa là 5."),
            ("瞋恚行人五煩惱，多行忿、恨、覆、慳、瞋，此謂五。",
             "Sân nhuế hành nhơn có 5 phiền não, đa hành phẫn, hận, phú, khan, sân."),
        ],
    )
    p = _replace_block(
        p, "3A_1366_1368",
        "與彼相應受想行識，是名相應。", "是謂離不善法。", 3,
        [
            ("與彼相應受想行識，是名相應。",
             "Cùng với tương ưng kia là thọ, tưởng, hành, thức. Đây gọi tên là tương ưng."),
            ("所起身口意業，此謂緣性。",
             "Chỗ khởi lên thân, ý, nghiệp. Đây gọi là duyên tánh."),
            ("以此三不善法，是為遠離、是出、是脫、是不相應，是謂離不善法。",
             "Mà 3 điều nầy là những pháp bất thiện. Đây nghĩa là viễn ly. Sự ra khỏi nầy là thoát, là bất tương ưng. Đây là lìa, là bất thiện pháp."),
        ],
    )

    # --- NHÓM 3A: Q5–Q6 ---
    p = _replace_block(
        p, "3A_1709_1710",
        "是捨是護。不退不進是心平等，此謂捨。", "五根為受捨。", 2,
        [
            ("是捨是護。不退不進是心平等，此謂捨。",
             "Đây xả, đây hộ; chẳng thối chẳng tiến, là tâm bình đẳng. Đây nghĩa là xả."),
            ("於是捨有八種，謂受捨、精進捨、見捨、菩提覺捨、無量捨、六分捨、禪枝捨、清淨捨。五根為受捨。",
             "Đối với xả nầy có 8 loại. Nghĩa là thọ xả, tinh tấn xả, kiến xả, bồ đề giác xả, vô lượng xả, lục phần xả, thiền chi xả, thanh tịnh xả, ngũ căn vi thọ xả."),
        ],
    )
    p = _replace_block(
        p, "3A_1762_1763",
        "答：想陰、行陰、識陰，此謂為身。", "此樂以身受，謂身受樂。", 2,
        [
            ("答：想陰、行陰、識陰，此謂為身。",
             "Đáp rằng: Tưởng ấm, hành ấm. Đây gọi là thân."),
            ("此樂以身受，謂身受樂。",
             "Niềm vui nầy mà thân thọ, tức thân thọ lạc."),
        ],
    )
    p = _replace_block(
        p, "3A_1771_1772",
        "第三者，依第二名為第三。", "二十二功德相應天居，生遍淨天。", 2,
        [
            ("第三者，依第二名為第三。第三禪者，是捨念、正智、樂、一心，此謂禪成就。",
             "Đệ tam nầy nương vào tên thứ 2 nên là thứ 3. Đệ tam thiền tức là xả niệm chánh trí, lạc nhứt tâm. Đây nghĩa là Thiền thành tựu."),
            ("入住者，彼已得第二禪，離一分五分，成就三種善十相具足，二十二功德相應天居，生遍淨天。",
             "Nhập trụ là kia được đệ nhị thiền. Lìa nhứt phần ngũ phần. Thành tựu 3 giống lành; 10 tướng đầy đủ; tương ưng với 22 công đức. Sanh vào cõi trời Biến Tịnh Thiên."),
        ],
    )
    p = _replace_block(
        p, "3A_1828_1829",
        "念者，謂念、隨念、正念，此謂為念。", "此謂捨念清淨。", 2,
        [
            ("念者，謂念、隨念、正念，此謂為念。",
             "Niệm nghĩa là niệm tùy niệm chánh niệm. Đây gọi là niệm."),
            ("以捨為念，成分明清白，此謂捨念清淨。",
             "Lấy xả làm niệm, thành phân minh thanh bạch. Đây gọi là xả niệm thanh tịnh."),
        ],
    )
    p = _replace_block(
        p, "3A_1893_1895",
        "答：是空入空界空穴，", "入虛空處心心數法，此謂虛空入。", 3,
        [
            ("答：是空入空界空穴，不為四大所觸，此謂為空。",
             "Đáp rằng: Đây là không nhập không giới, không chỗ. Chẳng vì sở thuộc vào tứ đại. Đây nghĩa là không."),
            ("於空正安心令滿無邊，此謂無邊。",
             "Đối với không chính là an tâm, làm cho đầy đủ vô biên. Đây nghĩa là vô biên."),
            ("無邊空者，是無邊空入，入虛空處心心數法，此謂虛空入。",
             "Vô biên không rồi vô biên không nhập. Nhập hư không xứ, tâm tâm số pháp. Đây nghĩa là hư không nhập."),
        ],
    )
    p = _replace_block(
        p, "3A_1957_1958",
        "越無所有處者，成越無所有處超入正度，", "此謂非非想處。", 2,
        [
            ("越無所有處者，成越無所有處超入正度，此謂越一切無所有處。",
             "Người vượt Vô sở hữu xứ thành vượt khỏi Vô sở hữu xứ siêu nhập vào chánh độ. Đây gọi là vượt tất cả Vô sở hữu xứ."),
            ("非非想者，彼無所有處寂寂作意修行餘定，此謂非非想處。",
             "Phi phi tưởng là nơi Vô sở hữu xứ kia tịch tĩnh tác ý, tu hành đủ định. Đây nghĩa là Phi phi tưởng xứ."),
        ],
    )
    p = _replace_block(
        p, "3A_2057_2058",
        "修彼心住不亂，此謂修。", "於青相放意為相，不除青想為味，作意無雙為處。", 2,
        [
            ("修彼心住不亂，此謂修。", "Tu nghĩa là giữ cho tâm kia trụ, chẳng loạn. Đây gọi là tu."),
            ("於青相放意為相，不除青想為味，作意無雙為處。",
             "Đối với tướng xanh lấy phóng ý làm tướng; chẳng trừ thánh tưởng làm vị; tác ý vô song làm xứ."),
        ],
    )
    p = _replace_block(
        p, "3A_2105_2106",
        "答：心於白相，此謂白一切入。", "於白相放意為相，不離白想為味，作意無二為處。", 2,
        [
            ("答：心於白相，此謂白一切入。彼修心住不亂，此謂修。",
             "Đáp rằng: Tâm lấy màu trắng làm tướng. Đây gọi là bạch nhứt thiết nhập; kia tu tâm ở chỗ chẳng loạn. Đây gọi là tu."),
            ("於白相放意為相，不離白想為味，作意無二為處。",
             "Đối với tướng trắng phóng ý làm tướng. Chẳng ly bạch tưởng làm vị. Tác ý vô nhị làm xứ."),
        ],
    )
    p = _replace_block(
        p, "3A_2256_2258",
        "答：潰爛者，或死二三宿潰爛膿出，", "作意不耐為處，等膖脹相功德。", 3,
        [
            ("答：潰爛者，或死二三宿潰爛膿出，猶如灌酪，身成潰爛，此謂潰爛。",
             "Đáp rằng: Hội Lạn là hoặc chết một hai đêm rồi như nát chảy ra nồng nặc; giống như nước sữa. Thân thành mục rữa. Đây có nghĩa là Hội Lạn."),
            ("於潰爛相以正智知，是謂潰爛相。",
             "Đối với tướng rữa thối nầy lấy chánh trí mà biết. Đây gọi là tướng mục rữa."),
            ("心住不亂此謂修，受持潰爛為相，厭為味，作意不耐為處，等膖脹相功德。",
             "Tâm trụ bất loạn nghĩa là tu. Thọ trì sự mục rữa là tướng. Xa lìa là vị. Tác ý chẳng nại là ý. Tướng sình trướng lên là công đức."),
        ],
    )
    p = _replace_block(
        p, "3A_2293_2294",
        "於棄擲想，是正智知，此謂棄擲想。", "作意不淨為處，膖脹想等功德。", 2,
        [
            ("於棄擲想，是正智知，此謂棄擲想。",
             "Đối với tưởng ném bỏ là dùng trí chơn chánh mà biết. Đây nghĩa là tưởng về sự ném bỏ."),
            ("心住不亂此謂修，受持棄擲想為想，厭為味，作意不淨為處，膖脹想等功德。",
             "Tâm trụ bất loạn đấy là tu. Thọ trì về tưởng ném bỏ là tưởng. Xa lìa là vị. Tác ý bất tịnh là xứ. Tưởng về sình trướng là công đức."),
        ],
    )
    p = _replace_block(
        p, "3A_2368_2370",
        "答：佛者，世尊自然無師，", "恭敬為味，增長信為處。", 3,
        [
            ("答：佛者，世尊自然無師，於未聞法正覺正諦，能知一切得力自在，此謂為佛。",
             "Đáp rằng: Đức Phật Thế Tôn tự nhiên chẳng có Thầy mà chứng. Đối với việc chưa nghe pháp mà chánh giác, chánh đế thì có thể biết rằng tất cả được lực tự tại. Đây gọi là Phật."),
            ("念佛世尊正遍知道菩提功德，念、隨念、念持、念不忘、念根、念力、正念，此謂念佛。",
             "Khi niệm Phật, Thế Tôn, bậc Chánh Biến Tri thì được công đức của Đạo Bồ Đề. Niệm tùy, niệm niệm, trì niệm, chẳng vọng niệm, căn niệm, lực chánh niệm. Đây nghĩa là niệm Phật."),
            ("心住不亂此謂修，令起佛功德為相，恭敬為味，增長信為處。",
             "Tâm trụ nơi chẳng loạn; đây nghĩa là tu. Làm cho khởi lên công đức của Phật; ấy là tướng. Cung kính là vị."),
        ],
    )
    p = _replace_block(
        p, "3A_2395_2396",
        "以明行足世尊成就，此謂明行具足。", "善逝者，到善路故，名曰善逝。", 2,
        [
            ("以明行足世尊成就，此謂明行具足。",
             "Chỗ làm bình đẳng được vô thượng tịch tĩnh; lấy Minh Hạnh Túc, Thế Tôn thành tựu. Đây nghĩa là Minh Hạnh đầy đủ."),
            ("善逝者，到善路故，名曰善逝。",
             "Thiện Thệ nghĩa là đến con đường lành; nên gọi là Thiện Thệ."),
        ],
    )
    p = _replace_block(
        p, "3A_2567_2568",
        "為他人得，捨自財物，此謂施。", "彼念、隨念、正念，此謂念施。", 2,
        [
            ("為他人得，捨自財物，此謂施。",
             "Làm vui lợi lạc cho người khác, làm cho người khác được xả bỏ tài vật của riêng mình. Đây gọi là thí."),
            ("以念施功德現念捨，彼念、隨念、正念，此謂念施。",
             "Dùng niệm thí công đức hiện ra niệm xả. Niệm kia tùy niệm, chánh niệm. Đây gọi là niệm thí."),
        ],
    )

    # --- NHÓM 3A: Q7–Q8 ---
    p = _replace_block(
        p, "3A_2660_2662",
        "隨逐者，攝算，以念無間逐出入息，", "應當隨觀，此謂隨觀。", 3,
        [
            ("隨逐者，攝算，以念無間逐出入息，此謂隨逐。",
             "Tùy theo đó mà nhiếp tâm vào sự đếm, lấy niệm chẳng gián đoạn, tùy theo đó mà hơi thở ra vào. Đây gọi là tùy toại."),
            ("名安置者，或鼻端、或於脣，是入出息所觸處，於彼作風相令念住，此謂安置。",
             "Cũng còn tên là an trí; hoặc nơi mũi, hoặc nơi môi. Đây gọi là hơi thở ra vào chỗ tiếp xúc. Đối với sự tạo ra gió kia, tướng ấy làm cho sự nhớ nghĩ trụ lại. Đây gọi là an trí."),
            ("名隨觀者，由觸自在，當隨觀相；於此所起喜樂等法，應當隨觀，此謂隨觀。",
             "Lại có tên là tùy quán. Do xúc tự tại và tùy theo tướng quán và đối với chỗ khởi hỷ lạc nầy so với pháp khác, nên tùy theo đó mà quán. Đây gọi là tùy quán."),
        ],
    )
    p = _replace_block(
        p, "3A_2673_2674",
        "若相已起住，以性應作意，此謂不愚癡。", "有時作長、有時作短，如是當修。", 2,
        [
            ("若相已起住，以性應作意，此謂不愚癡。",
             "Ngoài ra có tướng khởi lên việc trụ lại. Nếu tướng đã khởi trụ rồi thì lấy tánh ấy mà tác ý. Đây gọi là chẳng ngu si."),
            ("復次當為心消息，有時作長、有時作短，如是當修。",
             "Lại nữa nên làm cho tâm ta mất hơi đi. Có lúc dài hay có lúc ngắn. Cứ như thế mà hành trì."),
        ],
    )
    p = _replace_block(
        p, "3A_2719_2720",
        "知心者，此謂觀具足。", "以念安般受持地是修。", 2,
        [
            ("知心者，此謂觀具足。常見無常所初四行，此謂有時見。",
             "Biết tâm ở đây có nghĩa là quán sát đầy đủ, thường hay thấy vô thường là chỗ làm đầu tiên trong 4 việc. Đây gọi là có lúc thấy."),
            ("復次修者，以念安般受持地是修。",
             "Lại nữa người tu, lấy niệm An Ban làm chỗ thọ trì để tu."),
        ],
    )
    p = _replace_block(
        p, "3A_2768_2769",
        "依修眾生，此謂等死。", "名斷死者，謂阿羅漢，煩惱已斷。", 2,
        [
            ("依修眾生，此謂等死。", "Nương vào nơi chúng sanh vậy. Đây gọi là đẳng tử."),
            ("名斷死者，謂阿羅漢，煩惱已斷。",
             "Gọi tên là đoạn tử; nghĩa là A La Hán các phiền não đã đoạn rồi."),
        ],
    )
    p = _replace_block(
        p, "3A_2981_2982",
        "如是於一切眾生，慈心、饒益心，此謂慈。", "愛念為味，無嗔恚為起。", 2,
        [
            ("如是於一切眾生，慈心、饒益心，此謂慈。",
             "Khởi lên tâm làm lợi lạc. Như thế đối với tất cả chúng sanh. Lòng từ chính là tâm nhiêu ích. Đây nghĩa là lòng từ."),
            ("彼修住不亂，此謂修。令起饒益為相，愛念為味，無嗔恚為起。",
             "Làm cho kia tu giữ chẳng loạn; nên gọi là tu. Làm cho vui theo sự nhiêu ích khởi lên, lấy làm tướng."),
        ],
    )
    p = _replace_block(
        p, "3A_3004_3005",
        "答：忍辱是力、是鎧，", "唯應忍辱，是我所受。", 2,
        [
            ("答：忍辱是力、是鎧，能護身、能除忿恨，是稱譽，智人所嘆；是樂，令不退；是守護，令護一切具足；是曉了、令觀諸義，是名為起慚愧。",
             "Đáp rằng: Nhẫn nhục là cái lực, là cái áo giáp có thể hộ thân, có thể trừ sự giận dữ. Đây gọi là dự, là lời khen. Người trí tán thán chỗ ấy. Đây là niềm vui làm cho chẳng thoái. Đây là sự giữ gìn, làm cho hộ trì tất cả đầy đủ. Đây là ánh sáng làm cho thấy rõ nghĩa. Đây gọi là việc khởi lên sự xấu hổ."),
            ("復次當觀，我已剃頭，唯應忍辱，是我所受。",
             "Lại nữa nên quán ta đã cạo bỏ tóc râu; nên phải nhẫn nhục."),
        ],
    )
    p = _replace_block(
        p, "3A_3244_3246",
        "答：擇智自相內四大，此謂觀四大。", "通達空為味，除眾生想為起。", 3,
        [
            ("答：擇智自相內四大，此謂觀四大。",
             "Đáp rằng: Do trí cho biết là bên trong tự tướng gồm tứ đại. Đây nghĩa là xem thấy tứ đại."),
            ("彼心住不亂，此謂修。", "Tâm kia trụ nơi chẳng loạn. Đây nghĩa là tu."),
            ("隨觀四大為相，通達空為味，除眾生想為起。",
             "Tùy theo quán tứ đại lấy làm tướng. Thông đạt chỗ không, lấy làm vị."),
        ],
    )

    # --- NHÓM 3A: Q9–Q12 ---
    p = _replace_block(
        p, "3A_3488_3489",
        "復次是欲定勝行成就，此謂如意足。", "此謂修欲定勝行成就如意足。", 2,
        [
            ("復次是欲定勝行成就，此謂如意足。",
             "Tuy pháp kia như ý túc, lại lần lượt dục, định, thắng hạnh thành tựu. Đây có nghĩa là như ý túc."),
            ("為得如意，以初義修者，修彼法多修，此謂修欲定勝行成就如意足。",
             "Được như ý. Lấy nghĩa đầu nầy để tu vậy. Tu pháp kia, tu nhiều. Đây gọi là tu dục định thắng hạnh, thành tựu như ý túc."),
        ],
    )
    p = _replace_block(
        p, "3A_3713_3714",
        "除此三智餘慧，此謂等智。", "有慧非為聚非非為聚。", 2,
        [
            ("除此三智餘慧，此謂等智。", "Trừ 3 loại trí nầy, ngoài ra là huệ. Đây gọi là Đẳng trí."),
            ("復次四種慧：有慧為聚非為非聚、有慧為非聚非為聚、有慧為聚亦為非聚、有慧非為聚非非為聚。",
             "Lại nữa cũng có 4 loại huệ. Đó là hữu huệ vi tụ phi vi phi tụ; hữu huệ vi phi tụ phi vi tụ; hữu huệ vi tụ diệc vi phi tụ; hữu huệ phi vi tụ phi phi vi tụ."),
        ],
    )
    p = _replace_block(
        p, "3A_3719_3720",
        "現得厭欲，以慧達神通非達四諦，此謂波若。", "餘慧非為厭患亦非為達。", 2,
        [
            ("現得厭欲，以慧達神通非達四諦，此謂波若。",
             "Hiện tại được chỗ xa lìa sự ham muốn, dùng huệ đạt thần thông và không đạt Tứ Đế. Đây gọi là Bát Nhã."),
            ("為達非為厭患，於四道慧為厭患亦為達，餘慧非為厭患亦非為達。",
             "Vi đạt phi vi yểm hoạn. Đối với Tứ Đạo huệ vi yểm hoạn lại vi đạt. Ngoài ra huệ phi vi yểm hoạn lại phi vi đạt."),
        ],
    )
    p = _replace_block(
        p, "3A_3732_3733",
        "眼智為見，此謂義辯。", "於說法辭智，此謂辭辯。", 2,
        [
            ("眼智為見，此謂義辯。", "Lấy nhãn trí làm chỗ thấy. Đây nghĩa là Nghĩa Biện."),
            ("於說法辭智，此謂辭辯。", "Từ pháp từ trí, đây gọi là Từ Biện."),
        ],
    )
    p = _replace_block(
        p, "3A_3756_3757",
        "以是見色有對，依彼眼識起，此謂眼入。", "此清淨色謂為眼入。", 2,
        [
            ("以是見色有對，依彼眼識起，此謂眼入。",
             "Lấy sự thấy màu sắc mà có đối tượng. Nương vào nhãn thức kia để khởi lên. Đây gọi là nhãn nhập."),
            ("復次依眼睛肉揣白黑眼珠三圓，於肉血風痰唾五重內住，如半芥子，大如蟣子頭，初業所成、四大所造、火大最多，此清淨色謂為眼入。",
             "Lại nữa nương vào con mắt thịt đen trắng của nhãn châu để thấy gồm thịt, máu, gió, đờm, dãi. Trong đó chồng lên 5 lớp để ở như nửa hạt cải, lớn như đầu con kiến. Đầu tiên do nghiệp tạo thành rồi do tứ đại tạo ra lửa, to lớn hơn làm cho sáng tỏ ra màu sắc."),
        ],
    )
    p = _replace_block(
        p, "3A_3760_3761",
        "以是聞聲，於是聲有對，依耳識起，此謂耳入。", "四大所造清淨色，此謂耳入。", 2,
        [
            ("以是聞聲，於是聲有對，依耳識起，此謂耳入。",
             "Đó là nghe tiếng động, dùng âm thanh để đối lại và nương vào tai để khởi lên nhĩ thức. Đây gọi là nhĩ nhập."),
            ("復次於二孔赤毛為邊，依膜住，如青豆莖，初業所造、空大最多，四大所造清淨色，此謂耳入。",
             "Lại nữa, có hai lỗ có lông bên ngoài và nương vào các mô để ở như hạt đậu xanh. Nghiệp đầu tiên tạo ra chỗ trống thật lớn và do tứ đại là chỗ tạo tác ra màu trong sạch. Đây gọi là nhĩ nhập."),
        ],
    )
    p = _replace_block(
        p, "3A_3763_3764",
        "以是聞香，於是香有對，依鼻識起，此謂鼻入。", "四大所造清淨色，此謂鼻入。", 2,
        [
            ("以是聞香，於是香有對，依鼻識起，此謂鼻入。",
             "Đây do nghe mùi thơm và do mùi thơm nầy làm đối tượng. Nương vào mũi để khởi lên thức. Đây gọi là tỷ nhập."),
            ("復次於鼻孔中三和合，依細孔住，如拘毘陀羅形，初業所造、風大最多，四大所造清淨色，此謂鼻入。",
             "Lại nữa nơi lỗ mũi có 3 đường hòa hợp, nương vào chỗ lỗ nhỏ để ở, như hình Câu Tỳ Đà La (giao long). Đầu tiên do nghiệp tạo rồi gió lớn lên, tứ đại tạo ra màu thanh tịnh. Đây gọi là tỷ nhập."),
        ],
    )
    p = _replace_block(
        p, "3A_4239_4240",
        "無明緣行，行緣識，乃至生緣老死，", "復如是以輪可知。", 2,
        [
            ("無明緣行，行緣識，乃至生緣老死，如是皆苦陰起。於此皆苦陰無知，此謂無明。",
             "Vô minh duyên vào hành, hành duyên vào thức cho đến sanh duyên vào lão tử. Như vậy tất cả đều là khổ ấm khởi lên và làm cho khổ ấm nầy chẳng rõ. Đây nghĩa là vô minh."),
            ("無明緣行者，復如是以輪可知。",
             "Vô minh nương vào hành, lại như thế mà luân chuyển có thể rõ biết."),
        ],
    )
    p = _replace_block(
        p, "3A_4695_4696",
        "答：或於苦、或於集、或於滅、或於道、", "彼亦斷。", 2,
        [
            ("答：或於苦、或於集、或於滅、或於道、或於佛法僧、或初邊或後邊、或初後邊疑，或於因緣所起法彼疑惑，此謂疑。",
             "Đáp: Hoặc đối với khổ; hoặc đối với tập; hoặc đối với diệt; hoặc đối với Đạo; hoặc đối với Phật, Pháp, Tăng; hoặc đối với ban đầu hay ban cuối; hoặc sơ hậu liền nghi hoặc. Đối với nhơn duyên chỗ khởi lên pháp và sự nghi hoặc kia. Đây gọi là nghi."),
            ("彼亦斷。", "Cái kia lại cũng đoạn."),
        ],
    )
    p = _replace_block(
        p, "3A_4744_4745",
        "行滅此苦斷，不起餘苦，此謂苦邊。", "至於無動樂， 彼趣不可知。", 2,
        [
            ("行滅此苦斷，不起餘苦，此謂苦邊。",
             "Đây là làm cho hành diệt và khổ đoạn, chẳng khởi ra khổ nữa. Đây gọi là khổ biên."),
            ("是故說此偈：譬如槌打鐵， 火星流入水，次第成寂滅， 彼趣不可知。如是正解脫， 已度欲縛漏，至於無動樂， 彼趣不可知。",
             "Cho nên nói kệ như thế nầy. Giống như dập sắt nóng Hỏa tinh rơi vào nước Lần lượt thành tịch diệt Cõi kia chẳng thể rõ Như thế chánh giải thoát Độ được dục cột ràng Cho đến vô động lạc Cõi kia chẳng rõ biết."),
        ],
    )
    p = _replace_block(
        p, "3A_4834_4835",
        "復次解脫者唯道智；彼事為泥洹，此謂解脫門。", "十二不善心起。", 2,
        [
            ("復次解脫者唯道智；彼事為泥洹，此謂解脫門。",
             "Lại nữa giải thoát là chỉ có trí đạo. Việc ấy chính là Niết Bàn. Đây nghĩa là giải thoát môn."),
            ("煩惱者，一百三十四煩惱，如是三不善根、三覓、四漏、四結、四流、四厄、四取、四惡趣行、五慳、五蓋、六諍根、七使世間、八法、九慢、十煩惱處、十不善業道、十結、十邪邊、十二顛倒、十二不善心起。",
             "Còn phiền não có 134 loại phiền não. Như thế 3 bậc thiện căn, tam mịch, trí lậu, tứ kết, tứ lưu, tứ ách, tứ thủ, tứ ác thú hạnh, ngũ cái, lục tránh căn, thất sử thế gian, bát pháp, cửu mạn, thập phiền não xứ, 10 bất thiện nghiệp đạo, thập kết, thập tà biên, thập nhị điên đảo, thập nhị bất thiện tâm khởi."),
        ],
    )

    # --- NHÓM 3B: 19 cặp lệch ranh giới 1 vế dạng khác (2040-2041 đã sửa tại S1_13) ---
    p = _replace_block(
        p, "3B_1094_1095",
        "觀四大是名慧勝，以執著空故。", "如是以勝可知。", 2,
        [
            ("觀四大是名慧勝，以執著空故。",
             "Thọ nhiêu ích mà quán về tứ đại. Gọi là huệ thắng, lấy chấp trước không."),
            ("如是以勝可知。", "Nên như thế lấy thắng có thể biết."),
        ],
    )
    p = _replace_block(
        p, "3B_1317_1318",
        "於坐禪人若多起精進，過度處成心調，", "若多懈怠則欲睡眠。", 2,
        [
            ("於坐禪人若多起精進，過度處成心調，以二行應制伏心，以令精進起每中調適。若往婬處及種種相，增長調心，以二行折伏，以觀覓眾苦及惡果報。制伏懈心者，以二行成懈怠心。",
             "Đối với người tọa thiền nếu khởi nhiều sự siêng năng, quá độ xứ, thành tâm điều phục; lấy 2 việc làm nên chế phục tâm. Lấy tinh tấn khởi, mỗi mỗi thích nghi; nếu qua chỗ dâm và các tướng khác, tăng trưởng việc điều tâm; lấy 2 việc làm chiết phục, lấy quán các việc khổ và quả báo ác, chế phục tâm giải đãi; lấy 2 việc làm thành tâm giải đãi."),
            ("以不得勝定，令心無味，故成懈怠，若多懈怠則欲睡眠。",
             "Lấy chẳng được thắng định làm cho tâm vô vi nên thành giải đãi. Hoặc nhiều giải đãi tức muốn ngủ nghỉ."),
        ],
    )
    p = _replace_block(
        p, "3B_1374_1375",
        "離欲者，佛說為出。", "是故以欲和合煩惱。", 2,
        [
            ("離欲者，佛說為出。如得初禪，欲想相應作意成起，此退分法。",
             "Kẻ lìa dục, Phật nói là kẻ xuất ly; như được sơ thiền, dục tưởng tương ưng với tác ý thành tựu và khởi lên. Đây là thoái phần pháp."),
            ("是故以欲和合煩惱。", "Cho nên dục lấy hòa hợp với phiền não."),
        ],
    )
    p = _replace_block(
        p, "3B_1788_1789",
        "正定以樂枝麁，不能堪忍為得神通，", "見第四禪功德是其對治。", 2,
        [
            ("正定以樂枝麁，不能堪忍為得神通，第三禪不成勝分。",
             "Chánh định mà lạc chi thô. Chẳng thể kham nhẫn mà được thiền thông. Đệ tam thiền chẳng thành thắng phần."),
            ("如是見第三禪過患，見第四禪功德是其對治。",
             "Nên thấy đệ tam thiền ở đây quá hoạn. Thấy đệ tứ thiền là công đức. Đây là sự đối trị."),
        ],
    )
    p = _replace_block(
        p, "3B_1931_1932",
        "念無邊識定過患，爾時坐禪人已得識處，", "復見無所有處定功德。", 2,
        [
            ("念無邊識定過患，爾時坐禪人已得識處，自在欲起無所有處定，越於識處。",
             "Qua đến niệm vô biên thức định thì lúc bấy giờ người tọa thiền đã được thức rồi, tự tại dục khởi vô sở hữu xứ định, qua khỏi thức xứ."),
            ("復更思惟，識處定麁、無所有處定細，復見識處過患、復見無所有處定功德。",
             "Lại liền tư duy thức xứ định thô, vô sở hữu xứ định tế. Lại thấy thức xứ quá hoạn. Lại thấy vô sở hữu xứ định công đức."),
        ],
    )
    p = _replace_block(
        p, "3B_2651_2652",
        "由欲自在，念現入息、念現出息，起喜。", "念現入息、念現出息，起捨。", 2,
        [
            ("由欲自在，念現入息、念現出息，起喜。",
             "Do dự muốn tự tại mà nhớ đến hơi thở vào trong hiện tại và nhớ hơi thở ra trong hiện tại, khơi lên niềm vui."),
            ("已喜自在、已欲自在，念現入息、念現出息，起捨。",
             "Vui rồi tự tại, sự mong muốn tự tại rồi, nhớ nghĩ hơi thở vào trong hiện tại; nhớ nghĩ hơi thở ra trong hiện tại khởi lên xả."),
        ],
    )
    p = _replace_block(
        p, "3B_2859_2860",
        "如是此身所甞飲食，及雜涕唾屎尿臭穢，", "如是以流應念身自性。", 2,
        [
            ("如是此身所甞飲食，及雜涕唾屎尿臭穢，種種不淨，從九孔流溢，以多穿故、不成滿故。",
             "Như vậy thân nầy là chỗ chứa đồ ăn uống và tạp nhạp những nước hôi thối xú uế, gồm nhiều loại bất tịnh. Từ chín lỗ mà chảy ra, rồi sanh ra nhiều việc vậy, cũng chẳng trở thành đầy đủ."),
            ("如是以流應念身自性。",
             "Như thế mà lưu hành và nên nhớ nghĩ đến tự tánh của thân."),
        ],
    )
    p = _replace_block(
        p, "3B_3185_3186",
        "如是住慈悲喜，久復成捨攝受。", "如是作意修行於捨。", 2,
        [
            ("如是住慈悲喜，久復成捨攝受。",
             "Sau khi ở chung rồi tâm nầy thành tục, như thế giữ lại từ bi hỷ, sau đó trở thành xả nhiếp thọ."),
            ("如是作意修行於捨。", "Như thế tác ý tu hành đối với xả."),
        ],
    )
    p = _replace_block(
        p, "3B_3351_3352",
        "於是從業生四界。共生界展轉以四緣成緣，", "從食生可知。", 2,
        [
            ("於是從業生四界。共生界展轉以四緣成緣，所謂共生緣、展轉緣、依緣、有緣；餘界以緣成緣，所謂依緣、有緣。",
             "Đây là do nghiệp mà sanh ra 43 cảnh giới và cùng với các sự sanh ra, phát triển thay đổi để 4 duyên ấy duyên vào nhau. Cho nên gọi là những duyên cùng chung với nhau và những duyên thay đổi phát triển. Nương vào duyên và hữu duyên. Ngoài ra các giới lấy duyên để thành duyên, cho nên nương vào duyên để có duyên."),
            ("如是從心生、從時生、從食生可知。",
             "Như thế từ tâm sanh ra, từ thời gian sanh ra, từ ăn uống mà sanh ra, như thế phải nên biết."),
        ],
    )
    p = _replace_block(
        p, "3B_3531_3534",
        "以是修行心入第四禪，安詳出手摸日月，", "以他心智知梵天心。", 4,
        [
            ("以是修行心入第四禪，安詳出手摸日月，以智受持，此當成近手。",
             "Tâm được tự tại. Dùng sự thực hành nầy để vào đệ tứ thiền. Yên ổn mà ra như lấy tay xoa mặt trời mặt trăng. Dùng trí để thọ trì. Điều nầy có nghĩa là gần bàn tay."),
            ("彼成近手，彼坐禪人或坐或臥，以手摸捫日月，起身乃至梵世。",
             "Và vật kia sẽ trở thành bàn tay gần. Kẻ tọa thiền kia hoặc ngồi hoặc nằm như lấy tay xoa vào mặt trời mặt trăng, thân cao đến Phạm Thế."),
            ("彼坐禪人有神通，得心自在，樂行梵世。",
             "Kẻ tọa thiền kia có thần thông và tâm được tự tại, vui chơi nơi cõi Phạm Thế."),
            ("如是四如意足，以如是修行心，於遠受持近、於近受持遠，或多受持少、或少受持多，以天眼見梵天色，以天耳聞梵天聲，以他心智知梵天心。",
             "Như vậy là có Tứ Như Ý Túc. Việc nầy do tâm tu hành. Lấy xa đối với gần rồi lấy gần đối với xa. Hoặc lấy nhiều giữ gìn ít; hoặc lấy ít giữ gìn nhiều. Dùng thiên nhãn để thấy cõi sắc Phạm Thiên. Lấy thiên nhĩ để nghe tiếng Phạm Thiên. Lấy tha tâm trí để biết tâm của Phạm Thiên."),
        ],
    )
    p = _replace_block(
        p, "3B_3566_3567",
        "答：初坐禪人如是修四如意足，", "以耳界清淨，令心行增長。", 2,
        [
            ("答：初坐禪人如是修四如意足，以心得自在，入第四禪安詳出，次第依自性耳界，若遠聲作意聲相、或近聲作意聲相、若大聲作意大聲相、若細聲作意細聲相、若東方聲作意聲相，如是於一切方。",
             "Đáp rằng: Đối với người mới bắt đầu ngồi thiền như thế tu Tứ Như Ý Túc và dùng tâm để được tự tại. Nhập vào đệ tứ thiền rồi an tường mà xuất. Rồi lần lượt nương vào tự tánh của nhĩ giới; hoặc âm thanh xa tác ý về tướng nghe; hoặc âm thanh gần tác ý theo tướng nghe. Nếu tiếng lớn thì tác ý theo tướng của âm thanh lớn. Nếu âm thanh nhỏ, tác ý theo tướng của âm thanh nhỏ. Nếu âm thanh ở phía đông thì tác ý theo tướng của âm thanh đó. Như thế đối với tất cả nơi."),
            ("彼坐禪人如是以修行心清白，以耳界清淨，令心行增長。",
             "Với kẻ tọa thiền kia là người tu hành, tâm sẽ thanh tịnh trong sáng. Vì nhĩ giới thanh tịnh, làm cho tâm kia tăng trưởng."),
        ],
    )
    p = _replace_block(
        p, "3B_3812_3813",
        "此十法共生、不相離，此謂聚。", "是謂眼十。", 2,
        [
            ("此十法共生、不相離，此謂聚。",
             "Đây là 10 pháp cùng sanh sống chẳng lìa nhau. Đây gọi là sự tập họp."),
            ("是謂眼十。", "Nên gọi là 10 loại của mắt."),
        ],
    )
    p = _replace_block(
        p, "3B_3887_3888",
        "從意識界觸生受，以廣成一百八受，", "此謂受陰。", 2,
        [
            ("從意識界觸生受，以廣成一百八受，六依愛起受、六依出離起受、六依愛憂起受、六依出離憂起受、六依愛捨起受、六依出離捨起受。",
             "Từ ý tiếp xúc, sanh ra thọ. Từ ý thức giới tiếp nhận vào, sanh ra thọ. Từ đó nói rộng ra 108 loại thọ. 6 loại nương vào ái để khởi lên thọ. 6 loại nương vào sự ra khỏi, khởi lên thọ. 6 loại nương vào ái ưu tư khởi lên thọ. 6 loại nương vào sự ra khỏi ái ưu khởi lên thọ. 6 loại nương vào ái xả để khởi lên thọ. 6 loại nương vào sự xuất ly xả để khởi lên thọ."),
            ("此六六成三十六，於三時三三十六，此謂受陰。",
             "Đây là 6 lần 6 thành 36 loại. Lấy 3 thời (quá khứ, hiện tại, vị lai) nhơn cho 36 thành 108 loại thọ ấm."),
        ],
    )
    p = _replace_block(
        p, "3B_4135_4136",
        "彼思惟使，非智所處，", "無彼識為有滅。", 2,
        [
            ("彼思惟使，非智所處，為得有成住於有，如種在耕熟田。",
             "Hòa hợp cùng với sự có để suy nghĩ và sự suy nghĩ kia làm cho chẳng phải chỗ trí tuệ nương vào. Vì được hữu rồi thành ra trụ ở nơi hữu, như trồng giống ở ruộng lúa."),
            ("無彼識為有滅。", "Không có thứ kia làm cho có diệt."),
        ],
    )
    p = _replace_block(
        p, "3B_4179_4180",
        "幾果報？幾過去？", "幾未來？幾現在？", 2,
        [
            ("幾果報？", "Có bao nhiêu phần gọi là quả báo?"),
            ("幾過去？幾未來？幾現在？",
             "Có bao nhiêu phần thuộc về quá khứ, vị lai và hiện tại?"),
        ],
    )
    p = _replace_block(
        p, "3B_4324_4325",
        "問：不然。", "何故世尊說苦因滅？", 2,
        [
            ("問：不然。", "Hỏi: Như thế không đúng."),
            ("此亦集滅，何故世尊說苦因滅？",
             "Điều nầy lại như tập diệt. Vì sao Đức Thế Tôn lại nói khổ là nguyên nhơn diệt?"),
        ],
    )
    p = _replace_block(
        p, "3B_4364_4365",
        "此方便為實滅，第四說道。", "為滅病故，如病說藥。", 2,
        [
            ("此方便為實滅，第四說道。",
             "Đây là phương tiện làm thật diệt. Lần thứ 4 nói về đạo."),
            ("如明了醫，初見病源，後問病緣，為滅病故，如病說藥。",
             "Như một vị thầy thuốc rõ biết. Đầu tiên thấy rõ nguyên nhân của hạnh, sau đó liền hỏi bịnh duyên. Vì muốn cho lành bịnh; nên theo bệnh ấy nói để bốc thuốc."),
        ],
    )
    p = _replace_block(
        p, "3B_4425_4426",
        "以五種成。", "五根是道。", 2,
        [
            ("以五種成。", "Dùng 5 loại để thành."),
            ("五趣是苦，五蓋是集，斷蓋是滅，五根是道。",
             "Đó là 5 cõi chính là chỗ khổ. 5 sự che đậy ấy là tập; đoạn trừ những che đậy ấy đi gọi là diệt. Ngũ căn chính là Đạo."),
        ],
    )
    p = _replace_block(
        p, "3B_4825_4826",
        "何故？是人以無相，其心得脫。", "三解脫成所得。", 2,
        [
            ("何故？是人以無相，其心得脫。",
             "Tại sao người nầy dùng vô tướng? - Tâm nầy được giải thoát."),
            ("雖解脫彼已作，以執其已得無作解脫，三解脫成所得。",
             "Mà giải thoát kia đã làm rồi, lấy chấp vào cái nầy được vô tác giải thoát. Tam Giải Thoát thành chỗ được."),
        ],
    )
    return p


# Bảng chuẩn hóa lỗi dấu thanh kiểu cũ & lỗi gõ dấu từ bản in PDF gốc
VIET_TYPO_FIXES: List[Tuple[str, str]] = [
    (r"\blọan\b", "loạn"),
    (r"\bLọan\b", "Loạn"),
    (r"\bđọan\b", "đoạn"),
    (r"\bĐọan\b", "Đoạn"),
    (r"\bthóat\b", "thoát"),
    (r"\bThóat\b", "Thoát"),
    (r"\bnuơng\b", "nương"),
    (r"\bNuơng\b", "Nương"),
    (r"\btuờng\b", "tường"),
    (r"\bthuờng\b", "thường"),
    (r"\bđuợc\b", "được"),
    (r"\bnhiểm\b", "nhiễm"),
    (r"\bvể\b", "về"),
    (r"\bsụ\b", "sự"),
    (r"\bVô sỡ hữu\b", "Vô sở hữu"),
    (r"\bvô sỡ hữu\b", "vô sở hữu"),
    (r"\bngưới\b", "người"),
    (r"\bNgưởi\b", "Người"),
    (r"\bngưởi\b", "người"),
    (r"\btrhở\b", "trở"),
    (r"\btiênglớn\b", "tiếng lớn"),
    (r"\bđễ\b", "để"),
    (r"\bphiền ão\b", "phiền não"),
]


def normalize_gtdl_viet_text(text: str) -> str:
    """Tầng 4: Vệ sinh dấu câu, khoảng trắng dính và chuẩn hóa lỗi chính tả/dấu thanh PDF gốc."""
    v = text.strip()

    # 1. Xử lý hai dấu chấm liên tiếp '..' (bảo vệ dấu ba chấm '...')
    v = re.sub(r"(?<!\.)\.\.(?!\.)", ".", v)

    # 2. Xử lý dính dấu chấm không có khoảng trắng (ví dụ: 'phần.Đây', '10.Người'), bảo vệ 'v.v...'
    v = re.sub(r"\bv\.v\.\.\.", "#VV_DOTS#", v)
    v = re.sub(r"\bv\.v\.", "#VV_DOT#", v)
    v = re.sub(r"\.(?=[A-ZÀ-Ỹa-zà-ỹ])", ". ", v)
    v = v.replace("#VV_DOTS#", "v.v...").replace("#VV_DOT#", "v.v.")

    # 3. Xử lý dấu câu thừa/lỗi tổ hợp: '?,', '!;', '.;', gạch ngang lơ lửng cuối dòng '-'
    v = re.sub(r"([?!])\s*,", r"\1", v)
    v = v.replace(".;", ";")
    if v.endswith("-") and not v.endswith("--"):
        v = v[:-1].rstrip() + "."

    # 4. Chuẩn hóa lỗi đặt sai vị trí dấu thanh & lỗi gõ dấu từ bản in gốc
    for pat, rep in VIET_TYPO_FIXES:
        v = re.sub(pat, rep, v)

    v = re.sub(r"[ \t]+", " ", v).strip()
    return v


def refine_gtdl_pairs(pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Thực thi trọn bộ 4 tầng tinh chỉnh ranh giới câu và vệ sinh văn bản Giải Thoát Đạo Luận."""
    p = list(pairs)
    p = _apply_stage1_initial_30(p)
    p = _apply_stage2_clusters10(p)
    p = _apply_stage3_3a_3b(p)
    p = [(h.strip(), normalize_gtdl_viet_text(v)) for h, v in p]
    return p
