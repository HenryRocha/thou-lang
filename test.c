{
    maths x = 8;
    maths y = 9;
    maths z = 10;

    is_it_true test_bool_assign = z > y > x;
    thou_shalt_utter(test_bool_assign);

    thou_shalt_utter(thou_shalt_read());

    maths w = 0;

    thou_shall_repeat_if(x < (8 * 10))
    {
        shouldst_this_be_true(!w || 0)
        {
            x = x + 1;
        }
    }

    shouldst_this_be_true(1 == 1)
    {
        shouldst_this_be_true(2 == 3)
        {
            thou_shalt_utter(11);
        }
        if_naught shouldst_this_be_true(3 < 4)
        {
            thou_shalt_utter(22);
        }
        if_naught
        {
            thou_shalt_utter(33);
        }
    }

    kayne_west_phrase r1;
    r1 = "abc";
    kayne_west_phrase r2 = "ab";

    shouldst_this_be_true(r1 == r2)
    {
        thou_shalt_utter("É igual!");
    }
    if_naught
    {
        thou_shalt_utter("É diferente!");
    }

    kayne_west_phrase r3 = "aa";

    thou_shall_repeat_if(r3)
    {
        x = x + 10;
        r3 = "";
    }

    thou_shalt_utter(r3);
    thou_shalt_utter(x);
}
