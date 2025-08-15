//
//  settingView.swift
//  Camplate_iOS
//
//  Created by SeongYongSong on 8/15/25.
//

import SwiftUI

struct settingView: View {
    
    enum Theme: String, CaseIterable {
        case light = "Light"
        case dark = "Dark"
        case system = "System"
    }
 let UserId = "@soseoyo12"
    
    @State private var ID = ""
    @State private var Univ = "인하대학교"
    @State private var ThemeMode = Theme.light
    
    
    var body: some View {
        NavigationStack {
            Form {
                Section("내 정보"){
                    HStack {
                        Text("유저 ID")
                        Spacer()
                        Text("\(UserId)")
                            .foregroundColor(Color.gray)
                    }
                }
                
                Section("학교") {
                    NavigationLink {
                        selectUnivView()   // ← 바인딩 넘김
                    } label: {
                        HStack {
                            Text("내 학교")
                            Spacer()
                            Text(Univ).foregroundColor(.gray)
                        }
                    }
                }
                
                Section("테마"){
                        Picker("테마 설정", selection: $ThemeMode) {
                            ForEach(Theme.allCases, id: \.self) {
                                Text($0.rawValue)
                            }
                        }
                }
                .navigationTitle("설정")
            }
        }
    }
}

#Preview {
    settingView()
}
