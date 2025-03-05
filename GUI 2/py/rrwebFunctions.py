from flask import Flask, jsonify, request, send_file
import os
import shutil
import subprocess
import os
import json



def delete_jsons():
    jsons_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "jsons"))    # Adjust path if needed
    if os.path.exists(jsons_folder):
        shutil.rmtree(jsons_folder)  # Deletes the folder and its contents
        os.makedirs(jsons_folder)  # Recreate the empty folder
        return jsonify({"message": "jsons folder deleted"}), 200
    else:
        return jsonify({f"message": "jsons folder does not exist"}), 404


def generate_events():
    try:
        data = request.get_json()
        session_id = data.get("sessionId")
        
        if not session_id:
            return jsonify({"error": "Missing sessionId"}), 400

        session_folder = os.path.join("jsons", session_id)
        merged_path = os.path.join(session_folder, "merged_events.json")
        output_video = os.path.join(session_folder, "output.mp4")

        if not os.path.exists(merged_path):
            return jsonify({"error": "Merged events file not found"}), 404


        subprocess.run(["rrvideo", "--input", merged_path, "--output", output_video], 
                       check=True, 
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT,
                       shell=True)

        if not os.path.exists(output_video):
            return jsonify({"error": "Video file not found"}), 404

        return jsonify({"message": "Video generated successfully", "videoPath": f"{output_video}"}), 200

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Print the full error to console
        return jsonify({"error": str(e)}), 500

def download_video(session_id):
    session_folder = os.path.join("jsons", session_id)
    output_video = os.path.join(session_folder, "output.mp4")

    if not os.path.exists(output_video):
        return jsonify({"error": "Video file not found"}), 404

    return send_file(output_video, as_attachment=True, mimetype="video/mp4")

def save_json():
    try:
        data = request.get_json()
        session_id = data.get("sessionId")
        events = data.get("events")

        if not session_id or not events:
            return jsonify({"error": "Missing sessionId or events"}), 400

        # Create session folder
        session_folder = os.path.join("jsons", session_id)
        os.makedirs(session_folder, exist_ok=True)
        merged_path = os.path.join(session_folder,"merged_events.json")

        # Save individual events
        file_index=len(os.listdir(session_folder)) if len(os.listdir(session_folder)) >0 else 1

        file_path = os.path.join(session_folder, f"events{file_index}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

        # Create merge
        existing_events = []
        if os.path.exists(merged_path):
            # Load existing merged file
            with open(merged_path, "r", encoding="utf-8") as f:
                try:
                    existing_events = json.load(f)
                    if not isinstance(existing_events, list):  # Ensure it's a list
                        existing_events = []
                except json.JSONDecodeError:
                    print(":(")

        # Append new events and save back
        existing_events.extend(events)
        with open(merged_path, "w", encoding="utf-8") as fout:
            json.dump(existing_events, fout, indent=2)

        return jsonify({"message": "Saved successfully", "filePath": file_path})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
