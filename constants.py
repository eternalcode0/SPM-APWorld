"""Lists all constants (mostly strings) used by AP"""

from .names.region_names import RegionName as R


# TODO: Remove entrance names, they're constants only used once each in rules so no need to store them like this
class SPMEntrance:
    # region Flipside Entrances
    MAC09_L_3D_2_1 = "Flipside 1F - Layer 2 -> 1"
    MAC09_L_3D_2_3 = "Flipside 1F - Layer 2 -> 3"
    MAC09_L_3D_3_2 = "Flipside 1F - Layer 3 -> 2"
    # endregion

    # region Flopside Entrances
    # MAC11_DEFAULT  # Flopside 3F
    MAC11_DOKAN_1 = "Flopside 3F - Layer 2 - Right Pipe"  # MAC12_DOKAN_1
    # MAC11_PURE_HEART_RET
    MAC11_FALL_1 = "Flopside 3F - Layer 1 - Fall Into"  # There's not an exit for this so might need a spring


    MAC15_L_3D_1_2 = "Flopside B2 - Layer 1 -> 2"
    MAC15_L_3D_2_1 = "Flopside B2 - Layer 2 -> 1"

    MAC19_L_3D_1_2 = "Flopside 1F - Layer 1 -> 2"

    # MAC22_DEFAULT  # Flipside Tower Scene
    # MAC22_EPI_00  # Flipside Tower Postgame Cutscene

    # MAC30_DEFAULT  # Arcade
    MAC30_DOKAN = "Arcade - Pipe"  # MAC04_DOKAN
    # MAC30_END  # Arcade Menu
    # endregion

    # region Chapter 1 Entrances
    # HE101_DEFAULT  # Lineland Road
    HE101_IE_DOA_02 = f"{R.HE101} - Bestovius' House, Hidden Door"  # HE106_IE_DOA
    HE101_DOKAN_2 = f"{R.HE101} - Front Pipe near Bestovius' House"  # HE103_DOKAN_1
    HE101_DOKAN_3 = f"{R.HE101} - Back Pipe near Bestovius' House"  # N/A - Not Enterable
    HE101_DOA1_L = f"{R.HE101} - Chapter Door"  # N/A - Not Enterable
    HE101_DOA2_L = f"{R.HE101} - Sealed Door"  # HE102_DOA1_L

    # HE102_DOKAN_M  # Pipe under screen?
    HE102_DOA1_L = f"{R.HE102} - Left Door"  # HE101_DOA2_L
    HE102_DOA2_L = f"{R.HE102} - Right Door"  # HE104_DOA1_L

    # HE103_DEFAULT = "Lineland Road Underground"
    HE103_DOKAN_1 = f"{R.HE103} - Top Pipe"  # N/A - Not Enterable
    HE103_DOKAN_2 = f"{R.HE103} - Right Pipe"  # HE101_DOKAN_3

    # HE104_DEFAULT = "Lineland Road 3"
    HE104_DOA1_L = f"{R.HE104} - Left Door"  # HE102_DOA2_L
    HE104_DOA2_L = f"{R.HE104} - Right Door"  # HE105_DOA1_L

    # HE105_DEFAULT = "Lineland Road 4"
    HE105_DOA1_L = f"{R.HE105} - Left Door"  # HE104_DOA2_L

    # HE106_DEFAULT = "Lineland Road - Bestovius' Room"
    HE106_IE_DOA = f"{R.HE106} - Door"  # HE101_IE_DOA_02

    # Mount Lineland (1-2)
    # HE201_DEFAULT = f"{R.HE201} - Chapter start"
    # HE201_DOKAN_M = f"{R.HE101} - Pipe"
    HE201_DOA1_I = f"{R.HE201} - Right Door"  # HE202_DOA1_I
    HE201_DOA2_I = f"{R.HE201} - Hidden Shortcut Door"  # HE201_DOA2_I
    # HE201_  # Yeah there's no name for this entrance, it's the same as default ig

    # HE202_DEFAULT
    HE202_DOA1_I = f"{R.HE202} - Left Door"  # HE201_DOA1_I
    HE202_DOA2_I = f"{R.HE202} - Floating Door"  # N/A Not Enterable
    HE202_DOA3_I = f"{R.HE202} - Right Door"  # HE203_DOA1_I

    # HE203_DEFAULT
    HE203_DOKAN_1 = f"{R.HE203} - Pipe before Red's bridge"  # HE203_H_DOKAN_1
    HE203_DOKAN_4 = f"{R.HE203} - Pipe before Green's bridge"  # HE203_H_DOKAN_4
    HE203_H_DOKAN_1 = f"{R.HE203} - Left Background Pipe"  # HE203_DOKAN_1
    HE203_H_DOKAN_4 = f"{R.HE203} - Right Background Pipe"  # HE203_DOKAN_4

    # HE410_DEFAULT
    HE410_DOKAN_1 = f"{R.HE410} - Pipe"  # HE409_DOKAN_1
    HE410_DOA1_I = f"{R.HE410} - Door"  # HE411_DOA1_I

    # HE411_DEFAULT
    HE411_DOA1_I = f"{R.HE411} - Door"  # HE410_DOA1_I

    # HE412_DEFAULT
    HE412_DOA1_I =   # HE405_DOA3_I
    HE412_DOA2_I = f"{R.HE412} - Right Door"  # HE407_DOA1_I
    # endregion

    # region Chapter 2 Entrances
    # MI101_DEFAULT
    MI101_DOKAN_1 = f"{R.MI101} - Pipe"  # MI105_DOKAN_1
    MI101_DOA1_I = f"{R.MI101} - Locked Door"  # MI108_DOA1_I
    MI101_DOA2_I = f"{R.MI101} - Chapter Door"

    # MI102_DEFAULT
    MI102_DOA1_I = f"{R.MI102} - Bottom Door"  # MI110_DOA6_I
    MI102_DOA2_I = f"{R.MI102} - Top Door"  # MI110_DOA3_I

    # MI103_DEFAULT
    MI103_DOA1_I = f"{R.MI103} - Bottom Door"  # MI110_DOA5_I
    MI103_DOA2_I = f"{R.MI103} - Top Door"  # MI110_DOA4_I

    # MI104_DEFAULT
    MI104_DOA1_I = f"{R.MI104} - Door"  # MI110_DOA2_I

    # MI105_DEFAULT
    MI105_DOKAN_1 = f"{R.MI105} - Pipe"  # MI101_DOKAN_1

    # MI106_DEFAULT
    MI106_DOKAN_1 = f"{R.MI106} - Right Pipe"  # MI110_DOKAN_1
    MI106_DOKAN_2 = f"{R.MI106} - Left Pipe"  # MI107_DOKAN_1

    # MI107_DEFAULT
    MI107_DOKAN_1 = f"{R.MI107} - Pipe"  # MI106_DOKAN_2

    # MI108_DEFAULT
    MI108_DOKAN_1 = f"{R.MI108} - Pipe"  # MI108_HAI_DOKAN
    MI108_HAI_DOKAN = f"{R.MI108} - Background Pipe"  # MI108_DOKAN_1
    MI108_DOA1_I = f"{R.MI108} - Left Door"  # MI101_DOA1_I
    MI108_DOA2_I = f"{R.MI108} - Middle Door"  # MI109_DOA1_I
    MI108_DOA3_I = f"{R.MI108} - Right Door"  # MI111_DOA1_I

    # MI109_DEFAULT
    MI109_DOA1_I = f"{R.MI109} - Door"  # MI108_DOA2_I

    # MI110_DEFAULT
    MI110_DOKAN_1 = f"{R.MI110} - Pipe"  # MI106_DOKAN_1
    MI110_DOA1_I = f"{R.MI110} - Ground Door"  # MI111_DOA2_I
    MI110_DOA2_I = f"{R.MI110} - Left Elevated Door (Switch)"  # MI104_DOA1_I
    MI110_DOA3_I = f"{R.MI110} - Middle Left Elevated Door"  # MI102_DOA2_I
    MI110_DOA4_I = f"{R.MI110} - Middle Elevated Door"  # MI103_DOA2_I
    MI110_DOA5_I = f"{R.MI110} - Middle Right Elevated Door"  # MI103_DOA1_I
    MI110_DOA6_I = f"{R.MI110} - Right Elevated Door"  # MI102_DOA1_I

    # MI111_DEFAULT
    MI111_DOA1_I = f"{R.MI111} - Left Door"  # MI108_DOA3_I
    MI111_DOA2_I = f"{R.MI111} - Right Door"  # MI110_DOA1_I
    # endregion

    # region 2-2 Entrances
    # MI201_DEFAULT
    MI201_DOA_L = f"{R.MI201} - Mansion Front Door"
    # MI201_BANKEN = f"{R.MI201} - Kicked out of Mansion"  # Mimi kicks you out with the dogs
    # MI201_EVENT  # In the middle of the Merlee cutscene before she gives you the star

    # MI202_DEFAULT
    MI202_DOA_L = f"{R.MI202} - Mansion Front Door"
    MI202_DOA_02_L = f"{R.MI202} - Door Behind Curtains"

    # MI203_DEFAULT
    MI203_DOA1_L = f"{R.MI203} - Far Left Door"
    MI203_DOA2_L = f"{R.MI203} - Bottom Right, Left Door"
    MI203_DOA3_L = f"{R.MI203} - Top Right, Left Door"
    MI203_DOA4_L = f"{R.MI203} - Top Right, Middle Door"
    MI203_DOA5_L = f"{R.MI203} - Top Right, Right Door"
    MI203_DOA6_L = f"{R.MI203} - Bottom Right, Right Door"

    MI204_DOA2_L = f"{R.MI204} - Door"
    MI205_DOA2_L = f"{R.MI205} - Door"
    MI206_DOA2_L = f"{R.MI206} - Door"
    MI207_DOA2_L = f"{R.MI207} - Door"
    MI208_DOA2_L = f"{R.MI208} - Door"

    MI204_FALL = f"{R.MI204} - Pit Trap"
    MI205_FALL = f"{R.MI205} - Pit Trap"
    MI207_FALL = f"{R.MI207} - Pit Trap"
    MI209_DOKAN_1 = f"{R.MI209} - Pipe"
    MI210_DOKAN_1 = f"{R.MI210} - Pipe"
    MI211_DOKAN_1 = f"{R.MI211} - Pipe"

    # endregion
