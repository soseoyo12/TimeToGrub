//
//  selectUnivView.swift
//  Camplate_iOS
//
//  Created by SeongYongSong on 8/15/25.
//

import SwiftUI
import Foundation

struct selectUnivView: View {
    @State private var searchText = ""   // 검색어 저장
        let items = ["인하대학교", "서울대학교", "카이스트", "포항공과대학교", "연세대학교"]

        // 필터된 리스트
        var filteredItems: [String] {
            if searchText.isEmpty {
                return items
            } else {
                return items.filter { $0.localizedCaseInsensitiveContains(searchText) }
            }
        }

        var body: some View {
            
            }
            }

#Preview {
    selectUnivView()
}
