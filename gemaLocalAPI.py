import requests
import json
with open(r'resultEnglishSentences2.txt',"r",encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        url = "http://192.168.1.16:1234/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": "gemma-2-9b-it",
            "messages": [
                {"role": "user", "content": f"""Bạn có nhiệm vụ sửa tất cả các từ và tên không thuần Việt trong câu thành các tên địa điểm hoặc từ ngữ phù hợp và thuần Việt. Khi sửa xong, chỉ đưa ra kết quả đã sửa đúng, không giải thích hay thông tin gì thêm.
        Yêu cầu format:
        Input: [Câu gốc với từ không thuần Việt]
        Output: [input]->[Câu sau khi sửa]
        Ví dụ:
        Input: 28	Tấn: Ngày mai được không? Tôi sẽ lái xe từ showroom
        Output: 28	Tấn: Ngày mai được không? Tôi sẽ lái xe từ showroom->Tấn: Ngày mai được không? Tôi sẽ lái xe từ cửa hàng trưng bày
        ______
        Input: 350 Linh: Có suất chiếu lúc 7:30 tối tại Rạp chiếu phim Regal ở trung tâm thành phố.

        Output: 350 Linh: Có suất chiếu lúc 7:30 tối tại Rạp chiếu phim Regal ở trung tâm thành phố.-> Linh: Có suất chiếu lúc 7:30 tối tại Rạp chiếu phim Hoàng Gia ở trung tâm thành phố.
        _____
        thử với câu sau:
        {line}"""}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": True
        }

        # Make the request
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        merged_response = ""
        try:
        # Process the streamed response
            for chunk in response.iter_content(chunk_size=None):
                if chunk:  # Filter out keep-alive new chunks
                    # print(chunk.decode('utf-8'), end="")
                    chunk_str = chunk.decode('utf-8').lstrip('data: ').strip()
                    # print(chunk_str)
                    if(chunk_str!="[DONE]"):
                    # Parse the JSON from the chunk
                        parsed_chunk = json.loads(chunk_str)
                        
                        # Extract content from the 'choices' -> 'delta' -> 'content' field
                        delta = parsed_chunk["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        
                        # Append the content to the merged response
                        merged_response += content

            print(merged_response)
            with open("gemalLocal2.txt","a",encoding="utf-8")as f:
                f.write(merged_response.strip()+"\n")
        except Exception as e:
            print(e)
