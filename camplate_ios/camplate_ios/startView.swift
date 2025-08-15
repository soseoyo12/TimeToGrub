//
//  startView.swift
//  Camplate_iOS
//
//  Created by SeongYongSong on 8/14/25.
//

import SwiftUI

struct startView: View {
    var body: some View {
        Image("CamplateLogo")
            .resizable()
            .scaledToFit()
            .frame(width: 150, height: 150)
        Text("밥묵자")
            .font(.title)
    }
}

#Preview {
    startView()
}
