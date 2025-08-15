    //
//  mainView.swift
//  Camplate_iOS
//
//  Created by SeongYongSong on 8/14/25.
//

import SwiftUI


struct mainView: View {
    
    @State private var tapBounce = false


    
    var body: some View {
        
        NavigationStack{
            ScrollView{
                VStack{
            
                    ZStack (alignment: .topLeading){
                        
                        Rectangle()
                            .fill(Color.gray.opacity(0.1))
                            .frame(height: 450)
                            .cornerRadius(30)
                            .shadow(radius: 5, x : 0, y : 5)
                        
                        
                        VStack{
                            HStack (alignment: .firstTextBaseline) {
                                Image(systemName: "sun.max")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(height: 30)
                                    .padding(.leading, 25)
                                
                                Text("아침")
                                    .font(.title)
                                    .fontWeight(.medium)
                                
                                Text("(08:20-09:20)")
                                    .font(.caption)
                                    .padding(.bottom, 4.5)
                                
                                Spacer()
                                
                                Text("운영전")
                                    .padding(.horizontal, 10)
                                    .padding(.vertical,2)
                                    .background(Color.blue.opacity(0.2))
                                    .cornerRadius(10)
                                    .padding(.trailing)
                                
                                
                            }
                            
                            
                            Text("학생식당")
                                .fontWeight(.medium)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(.leading, 30)
                                .padding(.bottom)
                            
                            HStack {
                                Text("A")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("돈가스")
                                Spacer()
                                
                                
                            }
                            HStack {
                                Text("B")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("어묵볶음, 김치콩나물국, 맛김치")
                                Spacer()
                            }
                            HStack {
                                Text("C")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("요구르트")
                                Spacer()
                            }
                            Divider()
                                .padding(.horizontal)
                                .padding(.vertical, 5)
                            
                            
                            Text("학생식당")
                                .fontWeight(.medium)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(.leading, 30)
                                .padding(.bottom)
                            
                            HStack {
                                Text("A")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("돈가스")
                                Spacer()
                                
                                
                            }
                            HStack {
                                Text("B")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("어묵볶음, 김치콩나물국, 맛김치")
                                Spacer()
                            }
                            HStack {
                                Text("C")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("요구르트")
                                Spacer()
                            }
                            Divider()
                                .padding(.horizontal)
                                .padding(.vertical, 5)
                            
                            Text("학생식당")
                                .fontWeight(.medium)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(.leading, 30)
                                .padding(.bottom)
                            
                            HStack {
                                Text("A")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("돈가스")
                                Spacer()
                                
                                
                            }
                            HStack {
                                Text("B")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("어묵볶음, 김치콩나물국, 맛김치")
                                Spacer()
                            }
                            HStack {
                                Text("C")
                                    .fontWeight(.medium)
                                    .padding(.leading, 30)
                                Text("요구르트")
                                Spacer()
                            }
                            Divider()
                                .padding(.horizontal)
                                .padding(.vertical, 5)
                            Spacer()
                            
                        }
                    }
                }
                
            }
            .safeAreaInset(edge: .top) {
                VStack(alignment: .leading, spacing: 5) {
                    HStack(alignment: .firstTextBaseline) {
                        Text("인하대학교")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        Spacer()
                        NavigationLink {
                            settingView()
                        } label: {
                            Image(systemName: "gearshape")
                                .font(.title)
                                .padding(.horizontal)
                        }
                    }
                    
                    Text("2025년 8월 1일 (금)")
                        .font(.subheadline).fontWeight(.medium)
                                    .padding(.horizontal, 12).padding(.vertical, 6)
                                    .background(Color.black.opacity(0.08))
                                    .clipShape(RoundedRectangle(cornerRadius: 10))
                                    .padding(.horizontal, 15)
                }
                .padding(.bottom, 12)
                .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color(red: 0.86, green: 0.94, blue: 0.98))
                            .shadow(radius: 3)
                            .ignoresSafeArea(edges: .top)
                    )
            }
            
       
        }
        
        
        
        
        
        
    }
}

#Preview {
    mainView()
}
