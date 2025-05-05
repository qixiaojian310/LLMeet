package com.videomeeting.utils;
import org.apache.commons.lang3.RandomStringUtils;
public class IdGeneratorUtil {
    public static String generateCustomId() {
        String timePart = Long.toHexString(System.currentTimeMillis() % 1000000).toLowerCase();
        String randomPart1 = RandomStringUtils.randomAlphanumeric(4).toLowerCase();
        String randomPart2 = RandomStringUtils.randomAlphanumeric(4).toLowerCase();

        timePart = String.format("%6s", timePart).replace(' ', '0');

        return String.format("%4s-%4s-%4s-%4s",
                        timePart.substring(0, 4),
                        randomPart1,
                        randomPart2.substring(0, 2) + timePart.substring(4, 6),
                        RandomStringUtils.randomAlphanumeric(4).toLowerCase())
                .replace(' ', '0');
    }
}

