//
//  Data.swift
//  Camplate_iOS
//
//  Created by SeongYongSong on 7/30/25.
//

import Foundation


enum Time {
    case morning
    case afternoon
    case evening
}

enum MealTime {
    case breakfast
    case lunch
    case dinner
}

enum Restaurant {
    case 학식_한상한담
    case 학식_원플레이트
    case 학식_테이크아웃
    case 긱식_A
    case 긱식_B
    case 긱식_간편식
    case 교식_한상한담
    case 교식_마르쉐프
    case 교식_샐러드팩
    case 조식
    case 석식
}

struct Meal {
    let time: Time
    let date: String
    let mealTime: MealTime
    let restaurant: Restaurant
    let menu: String
    let price: Int
}

