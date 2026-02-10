import pytest
import tempfile

from data_utils import parse_tmx


@pytest.fixture
def xml_fixture():
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1" datatype="PlainText" segtype="sentence" adminlang="EN-US" srclang="be" o-tmf="LogiTermBT"/>
        <body>
            <tu>
                <prop type="ltattr-id">1</prop>
                <prop type="ltattr-match">1-1</prop>
                <tuv xml:lang="de" creationid="ALIGN!">
                    <seg>auf dem Gebiet der Steuern vom Einkommen und vom Vermögen</seg>
                </tuv>
                <tuv xml:lang="be" creationid="ALIGN!">
                    <seg>ў дачыненнi да падаткаў на даходы i маёмасць</seg>
                </tuv>
            </tu>
            <tu>
                <prop type="ltattr-id">1</prop>
                <prop type="ltattr-match">1-1</prop>
                <tuv xml:lang="be" creationid="ALIGN!">
                    <seg>Рэспублiка Беларусь i Федэратыўная Рэспублiка Германiя,</seg>
                </tuv>
                <tuv xml:lang="de" creationid="ALIGN!">
                    <seg>Die Bundesrepublik Deutschland und die Republik Belarus –</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(xml_content.encode("utf-8"))
        tmp.flush()
        print(tmp.name)
        yield tmp.name


def test_parse_tmx(xml_fixture):
    actual = parse_tmx(xml_fixture)
    expected = [
        [
            {
                "lang": "de",
                "text": "auf dem Gebiet der Steuern vom Einkommen und vom Vermögen",
            },
            {"lang": "be", "text": "ў дачыненнi да падаткаў на даходы i маёмасць"},
        ],
        [
            {
                "lang": "be",
                "text": "Рэспублiка Беларусь i Федэратыўная Рэспублiка Германiя,",
            },
            {
                "lang": "de",
                "text": "Die Bundesrepublik Deutschland und die Republik Belarus –",
            },
        ],
    ]
    assert actual == expected
