"""Module tinh chỉnh chuẩn xác các điểm lệch ranh giới câu và hỏi–đáp
cho tác phẩm Giải Thoát Đạo Luận (解脫道論 - Vimuttimagga, CV09).

Áp dụng cơ chế định vị theo ngữ cảnh nguyên văn (content-anchored block replacement)
để đảm bảo độ bền vững tuyệt đối, xử lý dứt điểm toàn bộ 21 vùng lệch ranh giới
cục bộ đã rà soát cùng 7 vùng lỗi đồng dạng phát hiện qua quét toàn cục (tổng 28 vùng):
- 21 vùng lệch ranh giới / trượt dòng trong Q1, Q2, Q3, Q5, Q6, Q7, Q8, Q9, Q12.
- 5 vùng lệch câu hỏi '何功德者，...' trong Q5 (Phẩm 8.2: Hỏa, Phong, Hoàng, Xích, Quang Minh).
- 1 vùng lỗi dấu hỏi bản Hán CBETA '何？處何功德？' tại Q6 (Phẩm 8.3: Trảm Trác Tướng).
- 1 vùng lệch chuỗi hỏi '何具足者 / 何非具足者 / 何事者' tại Q8 (Phẩm 8.5: Từ Tâm).
"""

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


def refine_gtdl_pairs(pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Áp dụng 28 khối tinh chỉnh ranh giới Hán – Việt trên toàn văn 12 Quyển."""
    p = list(pairs)

    # 1. Q1 - Phẩm 2 (dòng 297–299): Đưa 'Gọi nghĩa là Ba La Đề Mộc Xoa;' lên 297 & 'Oai nghi nầy bị che giấu.' lên 298
    p = _replace_block(
        p,
        "Q01_P02_297_299",
        "復次有學無學不動法波羅提木叉者，",
        "以此波羅提木叉威儀成就住者，護四威儀。",
        3,
        [
            (
                "復次有學無學不動法波羅提木叉者，是戒是起、是初、是行、是護、是威儀、是脫、是無縛、是諸法面，為正受善法，名波羅提木叉義。",
                "Lại nữa có học, vô học; bất động pháp Ba La Đề Mộc Xoa. Giới nầy là khởi. Việc đầu tiên là hành việc giữ gìn nầy là uy nghi. Sự thoát ra khỏi nầy là không bị trói buộc. Đây là các pháp bề mặt, làm chánh thọ thiện pháp. Gọi nghĩa là Ba La Đề Mộc Xoa.",
            ),
            (
                "不越身口業，是威儀所覆者。",
                "Chẳng vượt khỏi thân, khẩu, nghiệp. Oai nghi nầy bị che giấu.",
            ),
            (
                "以此波羅提木叉威儀成就住者，護四威儀。",
                "Lấy oai nghi Ba La Đề Mộc Xoa nầy thành tựu ở lại. Giữ gìn 4 oai nghi.",
            ),
        ],
    )

    # 2. Q2 - Phẩm 3 (dòng 603–604): Ghép '遇得處住' vào cùng câu hỏi '云何受？' khớp bản Việt
    p = _replace_block(
        p,
        "Q02_P03_603_604",
        "云何受？",
        "我從今日斷貪住處受遇得處。",
        2,
        [
            (
                "云何受？遇得處住，",
                "Thế nào gọi là thọ ngộ đắc xứ trụ?",
            ),
            (
                "不樂人所貪、不惱他令避，知是過患、見遇得處功德，我從今日斷貪住處受遇得處。",
                "Chẳng vui nơi người tham, chẳng buồn giận người khác làm cho xa lìa. Biết được điều sai trái nầy, thấy chỗ thích hợp có công đức, nên ta từ ngày hôm nay, đoạn lìa chỗ tham ở, thọ chỗ thích hợp.",
            ),
        ],
    )

    # 3. Q2 - Phẩm 3 (dòng 630–633): Chỉnh trượt lệch 4 dòng Nhất tọa thực / Tiết lượng / Vô sự xứ
    p = _replace_block(
        p,
        "Q02_P03_630_633",
        "若正食時，見象馬牛蛇、",
        "方便住聚落，不失無事處。",
        4,
        [
            (
                "若正食時，見象馬牛蛇、雨、和上、闍梨、客比丘來，方便而起，起已更食，不失一坐。",
                "Nếu lúc đang ăn mà thấy voi, ngựa, bò, rắn, Hòa Thượng A Xà Lê khách Tỳ Kheo đến, phương tiện mà qua khỏi, qua khỏi rồi mới ăn, chẳng mất một chỗ ngồi.",
            ),
            (
                "若節量食及時後食，無方便。",
                "Nếu biết lương thực và thời hậu thực không phải là phương tiện.",
            ),
            (
                "云何無事處方便？",
                "Thế nào gọi là vô sự xứ phương tiện?",
            ),
            (
                "或為受戒、懺罪、問法、布薩自恣、自病、看疾、問經疑處，如是等緣，方便住聚落，不失無事處。",
                "Hoặc là thọ giới sám tội, vấn pháp, Bố Tát, tự tứ, trị bịnh, khán bịnh. Hỏi rằng: Qua chỗ nghi là thế nào? Như thế các duyên, phương tiện ở trong làng xóm chẳng mất vô sự xứ.",
            ),
        ],
    )

    # 4. Q2 - Phẩm 3 (dòng 635–636): Trả 'Ngoài trụ xứ có thể ở.' về cuối dòng 635
    p = _replace_block(
        p,
        "Q02_P03_635_636",
        "若遇雨時宜入覆處，明相既現還而不失樹下。",
        "常坐不臥無方便。",
        2,
        [
            (
                "若遇雨時宜入覆處，明相既現還而不失樹下。露住、塚間，遇得此等方便，亦復如是，餘住處可住。",
                "Nếu gặp lúc mưa, liền vào núp bóng, khi dứt mưa liền trở lại như cũ mà chẳng mất. Dưới gốc cây, ở chỗ trống trải nơi gò mả, gặp chỗ thích nghi v.v... là phương tiện. Lại cũng như thế. Ngoài trụ xứ có thể ở.",
            ),
            (
                "常坐不臥無方便。",
                "Thường ngồi chẳng nằm là chẳng phải phương tiện.",
            ),
        ],
    )

    # 5. Q2 - Phẩm 3 (dòng 638–640): Căn chuẩn 3 dòng Tỳ Đàm bát đầu đà / Tiết lượng / Vô sự xứ nhiếp
    p = _replace_block(
        p,
        "Q02_P03_638_640",
        "如毘曇中說八頭陀，是時後不食攝。",
        "樹下、露坐、塚間，何故於無事處？",
        3,
        [
            (
                "如毘曇中說八頭陀，是時後不食攝。",
                "Như trong Tỳ Đàm nói là 8 loại Đầu Đà. Lúc ấy sau đó chẳng nhiếp về việc ăn.",
            ),
            (
                "節量、一坐，其所受持成一種類，是無事處攝。",
                "Tiết lượng một chỗ ngồi. Việc nầy thọ trì thành một thể loại. Đây gọi là vô sự xứ nhiếp.",
            ),
            (
                "樹下、露坐、塚間，何故於無事處？",
                "Nơi dưới gốc cây, chỗ ngồi trống và gò mả. Vì sao gọi là nơi vô sự?",
            ),
        ],
    )

    # 6. Q2 - Phẩm 5 (dòng 847–848): Đưa 'Đồng học nên đáp rằng:' xuống đầu dòng 848
    p = _replace_block(
        p,
        "Q02_P05_847_848",
        "以何功德一切所貴？應作如是問。",
        "得聞是已深思隨喜，當往彼處親覲受行。",
        2,
        [
            (
                "以何功德一切所貴？應作如是問。",
                "Việc làm nầy nếu làm, lấy gì là công đức tất cả chỗ quý; nên làm như thế và hỏi.",
            ),
            (
                "同學應答：某國某住某眾禪坐，某禪師眾所愛重。得聞是已深思隨喜，當往彼處親覲受行。",
                "Đồng học nên đáp rằng: Nước đó, ở chỗ ấy, chúng thiền tọa ấy, Thiền sư ấy v.v... được chúng ái trọng, được nghe điều nầy rồi nghĩ sâu, tùy hỷ, rồi đến chỗ kia thân cận học hỏi thọ lãnh.",
            ),
        ],
    )

    # 7. Q3 - Phẩm 6 (dòng 938–939): Trả 'Hai giới gần gũi, thành sân hành nhơn.' xuống đầu dòng 939
    p = _replace_block(
        p,
        "Q03_P06_938_939",
        "二界最近故成癡行人，所謂地界、水界。",
        "二界最近故成瞋行人，所謂火界、風界。",
        2,
        [
            (
                "二界最近故成癡行人，所謂地界、水界。",
                "Hai giới gần gũi vậy, thành si hành nhơn. Đó là địa giới và thủy giới.",
            ),
            (
                "二界最近故成瞋行人，所謂火界、風界。",
                "Hai giới gần gũi, thành sân hành nhơn. Đó là hỏa giới, phong giới.",
            ),
        ],
    )

    # 8. Q3 - Phẩm 7 (dòng 1052–1053): Trả 'trừ vô sắc nhứt thiết nhập.' lên cuối dòng 1052
    p = _replace_block(
        p,
        "Q03_P07_1052_1053",
        "答：九行處為神通緣，除無色一切入。",
        "八一切入，及分別虛空一切入。",
        2,
        [
            (
                "答：九行處為神通緣，除無色一切入。",
                "Đáp rằng: 9 hành xứ làm thần thông duyên, trừ vô sắc nhứt thiết nhập.",
            ),
            (
                "八一切入，及分別虛空一切入。",
                "Bát nhứt thiết nhập và phân biệt hư không nhứt thiết nhập.",
            ),
        ],
    )

    # 9. Q5 - Phẩm 8.2 (dòng 1682–1684): Căn chuẩn 3 dòng Nhị thiền (23 công đức / Như ở đầu đã nói rộng / Thiên trụ)
    p = _replace_block(
        p,
        "Q05_P08b_1682_1684",
        "入正受住者，成得第二禪，",
        "越人住故名為天住。",
        3,
        [
            (
                "入正受住者，成得第二禪，離於二枝，成就二枝三種善十相具足。",
                "Nhập chánh thọ trụ nghĩa là thành được đệ nhị thiền, lìa nơi 2 chi. Thành tựu 2 chi, 3 loại thiện và 10 tướng cụ túc.",
            ),
            (
                "二十三功德相應，是天住是功德，生光耀天。如初廣說。",
                "Tương ưng với 23 công đức. Đây là trụ nơi công đức ở cõi Trời. Sanh vào Quang Diệu Thiên, như ở đầu đã nói rộng.",
            ),
            (
                "天住者，從定生喜樂，越人住故名為天住。",
                "Ở cõi trời là từ định sanh hỷ lạc; qua khỏi cõi của người ở nên gọi tên là chỗ ở của Trời.",
            ),
        ],
    )

    # 10. Q5 - Phẩm 8.2 (dòng 1703–1704): Trả 'Đây nương vào tất cả nhập tướng tác ý, làm cho tâm hỷ diệt.' lên dòng 1703
    p = _replace_block(
        p,
        "Q05_P08b_1703_1704",
        "已觀二禪過患，復見三禪功德，",
        "不久以無喜樂令心得安解三禪枝。",
        2,
        [
            (
                "已觀二禪過患，復見三禪功德，是依一切入相作意，令喜心滅。",
                "Quán rồi nhị thiền quá hoạn. Lại thấy tam thiền công đức. Đây nương vào tất cả nhập tướng tác ý, làm cho tâm hỷ diệt.",
            ),
            (
                "以由喜樂受持心，如是作意，不久以無喜樂令心得安解三禪枝。",
                "Lấy mà do hỷ lạc thọ trì tâm, như thế tác ý. Chẳng chờ lấy vô hỷ lạc làm cho tâm được an ổn giải rõ nơi tam thiền chi.",
            ),
        ],
    )

    # 11. Q6 - Phẩm 8.3 (dòng 1940–1942): Căn chuẩn khối Vô Sở Hữu Xứ (gộp 2 câu '此謂無所有處' tương ứng bản dịch)
    p = _replace_block(
        p,
        "Q06_P08c_1940_1942",
        "越識處者，成越此識超入正度，",
        "入無所有處定心心數法，此謂無所有處。",
        3,
        [
            (
                "越識處者，成越此識超入正度，此謂越一切識處。",
                "Kẻ qua khỏi thức xứ, thành qua khỏi thức nầy siêu nhập vào chánh độ. Đây nghĩa là vượt lên tất cả thức xứ.",
            ),
            (
                "無所有者，不復修行、不復分別、成失彼識、但見無所有，此謂無所有處。入無所有處定心心數法，此謂無所有處。",
                "Kẻ Vô sở hữu chẳng lại tu hành, chẳng lại phân biệt, thành mất thức kia, thường thấy vô sở hữu. Đây nghĩa là Vô sở hữu xứ.",
            ),
        ],
    )

    # 12–16 (Bổ sung quét toàn cục). Q5 - Phẩm 8.2: 5 điểm lệch '何功德者，...' ở Hỏa, Phong, Hoàng, Xích, Quang Minh
    p = _replace_block(
        p,
        "Q05_P08b_2021_2022_Hoa",
        "火相巧於放意為相，",
        "如地一切入所說功德。",
        2,
        [
            (
                "火相巧於放意為相，不除火想為味，作意無雙為處。",
                "Tướng của lửa xảo; nên phóng ý là tướng. Chẳng trừ lửa tướng là vị. Tác ý vô song là xứ.",
            ),
            (
                "何功德者，不共五功德：於火一切入經營、起煙炎以光明想起、滅餘色光、隨意所燒、以作光明曉了於火界，如地一切入所說功德。",
                "Công đức gì vậy? Chẳng cùng với 5 công đức. Đối với hỏa nhứt thiết nhập kinh doanh, khởi lên ánh sáng và lấy ánh sáng đó làm tướng khởi. Mất ánh sáng rồi, tùy ý mà đốt. Lấy chỗ ánh sáng sớm rõ nơi hỏa giới. Như địa nhứt thiết nhập chỗ nói công đức.",
            ),
        ],
    )

    p = _replace_block(
        p,
        "Q05_P08b_2040_2041_Phong",
        "放意為相，不除風想為味，",
        "作意受持令清涼。",
        2,
        [
            (
                "放意為相，不除風想為味，作意無雙為處。",
                "Lấy phóng ý làm tướng; chẳng trừ gió tưởng làm vị. Tác ý vô song làm xứ.",
            ),
            (
                "何功德者，不同三功德，於風一切入風行自在、能令風起、作意受持令清涼。",
                "Công đức như thế nào? - Chẳng giống 3 công đức. Đối với gió tất cả nhập, gió làm tự tại, có thể làm cho gió khởi; tác ý thọ trì làm cho mát mẻ; như địa nhập nhứt thiết chỗ nói công đức.",
            ),
        ],
    )

    p = _replace_block(
        p,
        "Q05_P08b_2076_2077_Hoang",
        "於黃一切入放意是相，",
        "修黃一切入處處皆見黃。",
        2,
        [
            (
                "於黃一切入放意是相，不除黃想為味，作意無雙為處。",
                "Đối với hoàng nhứt thiết nhập phóng ý là tướng. Chẳng trừ hoàng tưởng là vị. Tác ý vô song là xứ.",
            ),
            (
                "何功德者，不同五功德，於黃一切入心隨逐得淨解脫，得黃除入作意，如金花種種黃色，修黃一切入處處皆見黃。",
                "Có công đức gì? - Chẳng đồng với 5 công đức. Đối với hoàng nhứt thiết nhập, tâm tùy toại được tịnh giải thoát, được màu vàng, trừ nhập tác ý. Như hoa màu vàng có nhiều loại màu vàng. Tu hoàng nhứt thiết nhập là nơi nơi đều thấy màu vàng.",
            ),
        ],
    )

    p = _replace_block(
        p,
        "Q05_P08b_2091_2092_Xich",
        "於赤相放意為相，",
        "如說於地一切入。",
        2,
        [
            (
                "於赤相放意為相，不離赤想為味，作意無二為處。",
                "Đối với tướng đỏ phóng ý làm tướng. Chẳng lìa đỏ tưởng làm vui. Tác ý vô nhị làm xứ.",
            ),
            (
                "何功德者，不共四功德，於赤一切入隨心得淨解脫，得赤除入，化種種赤色。不共功德者，如說於地一切入。",
                "Công đức như thế nào? - Chẳng cùng với 4 công đức. Đối với xích nhứt thiết nhập, tùy tâm được tịnh giải thoát, được xích trừ nhập; hóa ra nhiều loại màu đỏ chẳng cùng với công đức, như nói ở nơi địa nhứt thiết nhập.",
            ),
        ],
    )

    p = _replace_block(
        p,
        "Q05_P08b_2124_2125_QuangMinh",
        "光明放意為相，",
        "修光明一切入處處見光明。",
        2,
        [
            (
                "光明放意為相，不離光明想為味，作意無二為處。",
                "Ánh sáng phóng ý làm tướng. Chẳng lìa ánh sáng tưởng làm vị. Tác ý vô nhị làm xứ.",
            ),
            (
                "何功德者，與白功德等，修光明一切入處處見光明。",
                "Công đức gì? - Cùng với màu trắng công đức, tu quang minh nhứt thiết nhập; nơi nơi đều thấy ánh sáng.",
            ),
        ],
    )

    # 17 (Bổ sung quét toàn cục). Q6 - Phẩm 8.3 (dòng 2265–2266): Sửa lỗi dấu hỏi bản Hán CBETA '何？處何功德？' -> '何處？' / '何功德？'
    p = _replace_block(
        p,
        "Q06_P08c_2265_2266_CBETA_typo",
        "何？",
        "處何功德？",
        2,
        [
            ("何處？", "xứ nào?"),
            ("何功德？", "công đức gì?"),
        ],
    )

    # 18. Q6 - Phẩm 8.3 (dòng 2538–2539): Sửa lỗi dấu hỏi bản Hán CBETA '何？味何處？' -> '何味？' / '何處？'
    p = _replace_block(
        p,
        "Q06_P08c_2538_2539_CBETA_typo",
        "何？",
        "味何處？",
        2,
        [
            ("何味？", "vị gì?"),
            ("何處？", "xứ gì?"),
        ],
    )

    # 19. Q6 - Phẩm 8.3 (dòng 2545–2546): Trả 'Nhiều hoan hỷ dễ thương.' về cuối dòng 2545
    p = _replace_block(
        p,
        "Q06_P08c_2545_2546",
        "若人修行念戒成，得十二功德成，",
        "一切戒功德，是念戒功德。",
        2,
        [
            (
                "若人修行念戒成，得十二功德成，尊重師、重法、重僧、重戒學、重供養、重不放逸、於細微過患常見憂怖、護自身亦護他、從此世怖畏解脫、彼世怖畏解脫、多歡喜可愛。",
                "Nếu người tu hành niệm giới, thành được 13 công đức. Thành được những việc như tôn trọng Sư trưởng, trọng giáo pháp, trọng Tăng, trọng học giới, trọng việc cúng dường và trọng việc chẳng buông lung. Đối với việc lo sợ nhỏ nhoi cũng thường hay thấy lo sợ: gìn giữ cho chính mình và cũng gìn giữ cho người khác nữa. Từ đời nầy lo sợ việc giải thoát, cho đến đời khác cũng lo ngại việc giải thoát. Nhiều hoan hỷ dễ thương.",
            ),
            (
                "一切戒功德，是念戒功德。",
                "Với tất cả công đức của giới. Đây có nghĩa là công đức của việc niệm giới.",
            ),
        ],
    )

    # 20. Q6 - Phẩm 8.3 (dòng 2555–2556): Đưa 'Nên gọi tên là giới.' xuống đầu dòng 2556
    p = _replace_block(
        p,
        "Q06_P08c_2555_2556",
        "以餘行當念戒。",
        "是姓可貴，以財物自在。",
        2,
        [
            (
                "以餘行當念戒。",
                "Ngoài ra còn làm việc niệm giới.",
            ),
            (
                "名戒者，是樂無過患、是姓可貴，以財物自在。",
                "Nên gọi tên là giới. Đây là niềm vui chẳng lo sợ. Đây là tánh quý hóa; đây là tài vật tự tại.",
            ),
        ],
    )

    # 21. Q7 - Phẩm 8.4 (dòng 2762–2765): Chỉnh trượt lệch 4 dòng Niệm Tử
    p = _replace_block(
        p,
        "Q07_P08d_2762_2765",
        "何功德者，若修行念死，",
        "常觀世間心生厭患，此謂智相應念。",
        4,
        [
            (
                "何功德者，若修行念死，於上善法成不放逸、成憎不善法，於諸服飾不多受畜、心不慳悋，見身壽命心不貪著，作無常想、苦想、無我想皆令成滿，成向善趣向於醍醐，臨命將終心不謬誤。",
                "Công đức nào? - Nghĩa là nếu người tu hành nhớ đến việc chết thì lấy pháp lành cao nhất thành chẳng phóng dật, trở thành ghét pháp chẳng lành. Lấy đồ phục sức chẳng nhiều để mặc, tâm chẳng keo kiệt. Thấy thọ mệnh của thân, tâm chẳng tham trước, liền nghĩ đến vô thường, nhớ đến khổ và vô ngã. Tất cả đều làm cho đầy đủ, thành ra hướng đến cõi lành, hướng đến chỗ yên ổn. Khi lâm chung, tâm chẳng lầm lẫn.",
            ),
            (
                "云何修行？初坐禪人入寂寂坐，攝一切心，以不亂心念眾生死，我入死法、向於死趣、不過死法，如涅底履波陀脩多羅中說。若人樂觀死，當觀被殺人見死因緣。於是念死有四種：憂相應、驚相應、中人相應、智相應。",
                "Vì sao người tu hành mới tọa thiền nhập vào tịch tĩnh? Vì ngồi nhiếp tất cả tâm, lấy tâm bất loạn nhớ đến sự chết của chúng sanh. Ta vào trong pháp chết, hướng đến cõi chết; chẳng sợ pháp chết; giống như trong kinh Niết Đề Phúc Ba Đà đã nói: Nếu có người vui quán về sự chết thì hãy nên quán về kẻ bị giết và thấy nhơn duyên của sự chết, mà đối với niệm tử nầy có 4 loại. Tương ưng với lo, tương ưng với sợ, tương ưng với người khác và tương ưng với trí.",
            ),
            (
                "如喪愛子心生緣念，此謂憂相應；悲念童子卒暴命終，此謂驚相應念；如闍維人念離生故，此謂中相應念；常觀世間心生厭患，此謂智相應念。",
                "Như có tâm yêu mến con, tâm sanh duyên niệm. Đây gọi là tương ưng với lo. Thương nhớ con mình đã sớm mệnh chung. Đây gọi là niệm tương ưng với sự sợ hãi. Như người bị thiêu nhớ đến sự lìa sự sống vậy. Đây gọi là niệm tương ưng với người khác. Thường quan sát thế gian tâm sanh lo sợ. Đây gọi là niệm tương ưng của trí.",
            ),
        ],
    )

    # 22 (Bổ sung quét toàn cục). Q8 - Phẩm 8.5 (dòng 3085–3088): Căn chuẩn 4 dòng Từ tâm (何起者 / 何具足者 / 何非具足者 / 何事者)
    p = _replace_block(
        p,
        "Q08_P08e1_3085_3088",
        "何起者，是根令起。",
        "何事者，於眾生為事。",
        4,
        [
            (
                "何起者，是根令起。",
                "Khởi lên cái gì? - Căn nầy làm cho khởi.",
            ),
            (
                "何具足者，若慈成就，殺除瞋恚、除不善愛，令身口意業清淨，此謂具足。",
                "Đầy đủ thế nào? Nếu lòng từ thành tựu, giết trừ sân nhuế, trừ đi cái yêu thương chẳng lành, làm cho thân, miệng, ý nghiệp được thanh tịnh. Đây gọi là đầy đủ.",
            ),
            (
                "何非具足者，以二因失慈：以自朋生怨，以不善愛；以對治生怨，以起瞋恚，此謂非具足。",
                "Những gì là không đầy đủ? Dùng 2 nguyên nhân mất đi lòng từ; lấy chính người quen của mình rồi sanh oán, dùng cái ái không thuận; lấy sự đối trị sanh oán, lấy việc ấy khởi lên sân nhuế. Đây nghĩa là không đầy đủ.",
            ),
            (
                "何事者，於眾生為事。",
                "Việc gì? - Đối với tất cả chúng sanh là công việc vậy.",
            ),
        ],
    )

    # 23. Q8 - Phẩm 8.5 (dòng 3393–3394): Đưa '何修？' sang dòng 3394 khớp 'Tu cái gì, tướng gì?'
    p = _replace_block(
        p,
        "Q08_P08e2_3393_3394",
        "問：云何於食不耐想？何修？",
        "何相？",
        2,
        [
            (
                "問：云何於食不耐想？",
                "Hỏi rằng: Vì sao đối với việc ăn uống chẳng thể chịu theo tưởng?",
            ),
            (
                "何修？何相？",
                "Tu cái gì, tướng gì?",
            ),
        ],
    )

    # 24. Q9 - Phẩm 9 (dòng 3575–3577): Căn chuẩn 3 dòng Thiên Nhĩ
    p = _replace_block(
        p,
        "Q09_P09_3575_3577",
        "初坐禪人遠螺鼓等聲，",
        "不應作意於最可畏。",
        3,
        [
            (
                "初坐禪人遠螺鼓等聲，彼聲依自性耳，以天耳智應作意於聲相，令起天耳智。",
                "Người mới tọa thiền nghe được tiếng xa xa của ốc tù-và và tiếng trống v.v... Âm thanh kia nương vào nơi tự tánh của lỗ tai. Dùng thiên nhĩ trí nên tác ý với tướng của âm thanh. Làm cho khởi lên thiên nhĩ trí.",
            ),
            (
                "或細聲或大聲、或遠聲或近聲，唯天耳應取。",
                "Hoặc âm thanh nhỏ; hoặc âm thanh lớn; hoặc âm thanh xa; hoặc âm thanh gần. Chỉ có thiên nhĩ mới thuận tai.",
            ),
            (
                "於是初坐禪人，不應作意於最可畏。",
                "Đối với kẻ sơ thiền chẳng nên tác ý đối với việc quá sợ.",
            ),
        ],
    )

    # 29 (Bổ sung quét toàn cục). Q9 - Phẩm 9 (dòng 3626–3627): Đưa 'Có bao nhiêu loại thiên nhãn?' xuống dòng 3627
    p = _replace_block(
        p,
        "Q09_P09_3626_3627",
        "答：光明為九、或光明為五、",
        "業果報所成、修行所成。",
        2,
        [
            (
                "答：光明為九、或光明為五、或光明一切入事，於第四禪得自在，有眼性是其所能起。",
                "Đáp rằng: Ánh sáng ấy có 9 thứ. Hoặc ánh sáng ấy có 5; hoặc ánh sáng ấy gồm tất cả mọi việc. Đối với đệ tứ thiền được tự tại có được nhãn tánh thì từ đây có thể khởi lên được.",
            ),
            (
                "幾種天眼者，答二種天眼，業果報所成、修行所成。",
                "Có bao nhiêu loại thiên nhãn? Đáp rằng: Có 2 loại thiên nhãn do nghiệp quả báo mà thành hoặc do tu hành mà thành.",
            ),
        ],
    )

    # 30 (Bổ sung quét toàn cục). Q11 - Phẩm 11.2 (dòng 4346–4349): Căn chuẩn 4 dòng Thế Đế / Xuất Thế Đế
    p = _replace_block(
        p,
        "Q11_P11b_4346_4349",
        "問：云何？世諦果苦，集世諦因，",
        "此四聖諦，以十一行可勝可知。",
        4,
        [
            (
                "問：云何？世諦果苦，集世諦因，果滅，出世諦果。",
                "Hỏi: Những gì là Thế Đế quả, khổ tập thế đế nhơn quả? Đáp: Diệt xuất Thế Đế quả.",
            ),
            (
                "道，出世諦因。是故四，不三不五。",
                "Đạo xuất Thế Đế nhơn, rồi duyên vào nhau mà làm 4. Chứ chẳng phải 3 hay 5.",
            ),
            (
                "復次應知、應斷、應證、應修，以四句故成四。",
                "Lại nữa nên biết, nên đoạn, nên chứng, nên tu. Dùng 4 câu ấy nên trở thành 4.",
            ),
            (
                "此四聖諦，以十一行可勝可知。",
                "Đây là Tứ Thánh Đế lấy 11 hành có thể khá biết rõ hơn.",
            ),
        ],
    )

    # 25. Q12 - Phẩm 12.2 (dòng 4893–4901): Căn chuẩn toàn bộ 9 dòng Quả Chánh Thọ
    p = _replace_block(
        p,
        "Q12_P12b_4893_4901",
        "爾時人來，為日所曝，熱乏渴愛。",
        "二緣為起：作意一切相，及無相界不作意。",
        9,
        [
            (
                "爾時人來，為日所曝，熱乏渴愛。彼人見井知有水，彼不以身觸住。如是我長老有滅為泥洹，如實正智善見，我非阿羅漢漏盡。",
                "Lúc ấy có người đến và trời nóng nên khát nước, người kia thấy giếng, biết là có nước mà kẻ kia chẳng dùng tự thân của mình để tự biết, như thế Trưởng Lão có diệt Niết Bàn, như thật chánh trí thiện kiến. Ta chẳng phải A La Hán lậu tận.",
            ),
            (
                "何故令起者，答：為現見法樂住令起。如世尊教阿難，是時阿難如來不作意，一切諸相唯一受滅，無相心定令起住，是時阿難如來身成安隱。",
                "Vì sao mà làm cho khởi lên được? Đáp: Vì hiện thấy pháp lạc trú nên khởi, như Đức Thế Tôn đã dạy Ngài A Nan: Lúc ấy Ngài A Nan đối với Đức Như Lai không tác ý về tất cả các tướng, duy chỉ có một thọ diệt, tâm vô tướng định làm cho khởi lên trụ. Lúc ấy Ngài A Nan thành thân Như Lai an ổn.",
            ),
            (
                "云何以令起者，答：彼坐禪人入寂寂住，或住或臥，樂得果正受。作生滅見所初觀諸行，乃至性除智，性除智無間於泥洹果正受令安，依其禪成修道是。",
                "Và vì sao mà làm cho khởi lên? Đáp: Kẻ tọa thiền kia nhập vào sự tịch tịnh rồi đứng, hoặc ngồi, hoặc nằm vui với quả chánh thọ vừa được; tạo ra sự sanh diệt nơi chỗ thấy. Đầu tiên quán về các hành cho đến tánh trừ trí. Tánh trừ trí không gián đoạn. Đối với quả Niết Bàn làm cho an ổn. Nương vào nơi thiền nầy thành con đường để tu vậy.",
            ),
            (
                "是禪成所作，是名果正受。",
                "Thiền nầy thành chỗ tạo tác. Đây nghĩa là quả chánh thọ.",
            ),
            (
                "云何作意者，答：無為醍醐界以寂作意。",
                "Thế nào là tác ý? Đáp: Vô vi đề hồ giới lấy sự yên lặng mà tác ý.",
            ),
            (
                "彼成就幾緣？幾緣為住？幾緣為起？",
                "Cái kia sẽ thành tựu bao nhiêu duyên; bao nhiêu duyên trụ; bao nhiêu duyên để khởi?",
            ),
            (
                "答：彼正受二緣，不作意一切諸相，於無相界作意。",
                "Đáp: Chánh thọ kia có 2 duyên. Đó là bất tác ý tất cả các tướng và đối với vô tướng giới tác ý.",
            ),
            (
                "三緣為住：不作意一切諸相，於無相界作意，及初行。",
                "Ba duyên để trụ gồm bất tác ý tất cả các tướng; đối với vô tướng giới tác ý và sơ hành.",
            ),
            (
                "二緣為起：作意一切相，及無相界不作意。",
                "2 duyên cùng khởi: Tác ý tất cả tướng và vô tướng giới bất tác ý.",
            ),
        ],
    )

    # 26. Q12 - Phẩm 12.2 (dòng 4922–4928): Căn chuẩn toàn bộ 7 dòng Diệt Tận Định (phần 1)
    p = _replace_block(
        p,
        "Q12_P12b_4922_4928",
        "答：不生心心數法，此謂滅想受定。",
        "以奢摩他力、以毘婆舍那力。",
        7,
        [
            (
                "答：不生心心數法，此謂滅想受定。",
                "Đáp: Chẳng sanh tâm, tâm số pháp. Đây nghĩa là diệt tưởng thọ định.",
            ),
            (
                "誰令起定者，答：阿羅漢及阿那含，於此定作滿。",
                "Ai đã làm cho khởi định nầy? Đáp: A La Hán và A Na Hàm. Đối với định nầy đã đầy đủ.",
            ),
            (
                "誰不令起者，答：凡夫人及須陀洹、斯陀含，及生無色界人，於是非其境界故。",
                "Ai chẳng khởi lên? Đáp: Kẻ phàm phu và Tu Đà Hoàn, Tư Đà Hàm và người sanh ở cõi vô sắc giới. Đối với đây chẳng phải là cảnh giới vậy.",
            ),
            (
                "凡夫不能起煩惱障礙定，未斷故。",
                "Kẻ phàm phu chẳng nên khởi phiền não, chướng ngại định, vì chưa đoạn vậy.",
            ),
            (
                "須陀洹、斯陀含不能起，為更起。",
                "Tu Đà Hoàn, Tư Đà Hàm chưa nên khởi thì liền làm cho khởi lên.",
            ),
            (
                "非其處故，入無色界不能起。",
                "Chẳng phải là chỗ nầy vậy, nhập vô sắc giới chẳng nên khởi.",
            ),
            (
                "幾力成就令起者，答：以二力成就令起，以奢摩他力、以毘婆舍那力。",
                "Có bao nhiêu lực thành tựu làm cho khởi? Đáp: Lấy 2 lực thành tựu làm cho khởi. Đó là Xa Ma Tha lực và Tỳ Bà Xá Na lực.",
            ),
        ],
    )

    # 27. Q12 - Phẩm 12.2 (dòng 4935–4947): Căn chuẩn 13 dòng Diệt Tận Định (phần 2: Sơ tứ sự & Bảo hộ thân)
    p = _replace_block(
        p,
        "Q12_P12b_4935_4947",
        "於是入二禪覺觀，口行成所除；",
        "如長老舍利弗、如長老白鷺子底沙。",
        13,
        [
            (
                "於是入二禪覺觀，口行成所除；入第四禪出息入息，身行成所除；入滅想受定人，想受心行成所除。",
                "Đối với đây nhập nhị thiền, giác quán khẩu hạnh, thành sở trừ. Nhập đệ tứ thiền hơi thở vào ra là thân hành, thành sở trừ. Người nhập diệt tưởng thọ định thì tưởng thọ tâm hành thành sở trừ.",
            ),
            (
                "初幾事者，答：初四事，一縛、不亂、遠分別、觀事非事。",
                "Đầu tiên có bao nhiêu việc? Đáp: Đầu tiên có 4 việc. Sự trói buộc chẳng loạn, xa phân biệt, quán sự phi sự.",
            ),
            (
                "於是名一縛者，鉢袈裟一處[怡-台+(噗-口)]受持。",
                "Đây tên là một sự trói buộc. Bát, Cà Sa một xứ, mang theo.",
            ),
            (
                "不亂者，以所有方便，此身願莫生亂受持。",
                "Chẳng loạn. Đây là phương tiện sở hữu. Thân nầy nguyện chưa sanh loạn thọ trì.",
            ),
            (
                "遠分別者，稱其身力，以日作分別受持，於此久遠過期當起。",
                "Viễn phân biệt là xưng tụng thân lực nầy. Dùng số ngày để phân biệt thọ trì. Đối với thời kỳ xa xôi sẽ khởi lên.",
            ),
            (
                "觀事非事者，未至時分別。或眾僧為事和合，以彼聲我當起受持。",
                "Quán sự phi sự nghĩa là chưa tới thời để phân biệt; hoặc chúng tăng vì sự hòa hợp dùng tiếng kia, ta sẽ khởi thọ trì.",
            ),
            (
                "於是一縛者，為守護袈裟。",
                "Nơi một sự trói buộc nầy, vì giữ gìn Cà Sa.",
            ),
            (
                "不亂者及久遠分別，為守護身。",
                "Nên chẳng loạn và phân biệt xa xôi, vì bảo hộ thân.",
            ),
            (
                "觀事非事者，為不妨眾僧和合，住無所有處，或初作事入初禪。",
                "Quán sự phi sự là vì không phường chúng tăng hòa hợp, trụ vô sở hữu xứ; hoặc sơ tác nhập sơ thiền.",
            ),
            (
                "何故令起？",
                "Vì sao lại làm cho khởi?",
            ),
            (
                "答：為現法樂住者，是聖人最後無動定。復為起神通入廣定。",
                "Đáp: Vì hiện pháp lạc trú vậy. Đó là Thánh nhơn tối hậu vô động định, lại vì khởi thần thông nhập vào quảng định.",
            ),
            (
                "如長老正命羅漢，為守護身。如長老舍利弗、如長老白鷺子底沙。",
                "Như Trưởng Lão chánh mệnh A La Hán. Vì bảo hộ thân như Trưởng Lão Xá Lợi Phất, như Trưởng Lão Bạch Lộ Tử Đề Sa.",
            ),
        ],
    )

    # 28. Q12 - Phẩm 12.2 (dòng 4954–4961): Căn chuẩn toàn bộ 8 dòng trượt nặng cuối Diệt Tận Định
    p = _replace_block(
        p,
        "Q12_P12b_4954_4961",
        "云何心以起者，若阿那含人以阿那含果心起，",
        "云何此定有為無為者，答：不可說此定有為無為。",
        8,
        [
            (
                "云何心以起者，若阿那含人以阿那含果心起，若阿羅漢人以阿羅漢心起。",
                "Vì sao tâm lại khởi? Nếu người A Na Hàm thì dùng A Na Hàm quả để tâm khởi. Nếu người A La Hán thì dùng tâm A La Hán để khởi.",
            ),
            (
                "起已彼心何所著？",
                "Khởi rồi tâm kia dính mắc vào cái gì?",
            ),
            (
                "答：心專緣寂寂。",
                "Đáp: Tâm chuyên duyên vào sự tịch tịnh.",
            ),
            (
                "幾觸所觸者，答：三觸所觸，以空觸、無相觸、無作觸。",
                "Có bao nhiêu xúc sở xúc? Đáp: Có 3 loại xúc sở xúc. Dùng không xúc, vô tướng và vô tác xúc.",
            ),
            (
                "云何初起諸行？彼從身行、從彼口行。",
                "Vì sao sở khởi các hạnh? Từ kia thân làm, từ kia khẩu làm.",
            ),
            (
                "死人及入滅想定人何差別者，死人，三行沒無現，壽命斷、煖斷、諸根斷。",
                "Người chết và người nhập diệt tưởng định có gì sai biệt? Kẻ chết thì 3 việc kia mất không còn gì nữa nơi mạng sống; đoạn hơi ấm, đoạn các căn và đoạn nhập.",
            ),
            (
                "入受想定人，三行斷沒，壽命不斷、煖不斷、諸根不異。",
                "Người thọ tưởng định 3 việc làm ấy đoạn; nhưng thọ mệnh không mất; hơi ấm chẳng mất, các căn không khác.",
            ),
            (
                "此彼差別。",
                "Chính đây là sự sai biệt.",
            ),
            (
                "云何此定有為無為者，答：不可說此定有為無為。",
                "Vì sao định nầy hữu vi và vô vi? Đáp: Khó thể nói đây là định hữu vi hay vô vi.",
            ),
        ],
    )

    return p
