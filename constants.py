"""Lists all constants (mostly strings) used by AP"""

from .names.region_names import RegionName as R


# TODO: Remove entrance names, they're constants only used once each in rules so no need to store them like this
class SPMEntrance:
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
