import PhotosUI

struct PhotoReasoningScreen: View {
    @State private var image: UIImage?
    @State private var result = ""

    var body: some View {
        VStack {
            PhotosPicker("Choose Image", selection: .constant(nil), matching: .images) {
                Text("Select an Image")
            }
            .onChange(of: image) { _ in
                analyzeImage()
            }

            if let img = image {
                Image(uiImage: img).resizable().scaledToFit().frame(height: 200)
            }

            Text(result).padding()
        }
        .padding()
    }

    func analyzeImage() {
        guard let imgData = image?.jpegData(compressionQuality: 0.8),
              let url = URL(string: "https://api.kubu-hai.com/photo-reason") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("image/jpeg", forHTTPHeaderField: "Content-Type")
        request.httpBody = imgData

        URLSession.shared.dataTask(with: request) { data, _, _ in
            guard let data = data,
                  let response = try? JSONDecoder().decode([String: String].self, from: data),
                  let reasoning = response["analysis"] else { return }

            DispatchQueue.main.async {
                result = reasoning
            }
        }.resume()
    }
}
