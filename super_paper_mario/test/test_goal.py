from ..names import ItemName as I
from ..names import LocationName as L
from . import SPMTestBase


class TestGoal(SPMTestBase):
    def test_goal(self) -> None:
        self.assertAccessDependency(
            [L.CHAPTER_8_4_END],
            [
                [
                    I.RED_PURE_HEART,
                    I.PURPLE_PURE_HEART,
                    I.BLUE_PURE_HEART,
                    I.CYAN_PURE_HEART,
                    I.GREEN_PURE_HEART,
                    I.WHITE_PURE_HEART,
                    I.ORANGE_PURE_HEART,
                    I.YELLOW_PURE_HEART,
                ]
            ],
            True,
        )
