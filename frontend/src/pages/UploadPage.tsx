import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import { Upload, FileText, X, Loader2, CheckCircle2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import api from "@/lib/api";
import { formatFileSize } from "@/lib/utils";
import { toast } from "sonner";
import type { Resume } from "@/types";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedResume, setUploadedResume] = useState<Resume | null>(null);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const f = acceptedFiles[0];
    if (f) {
      const validTypes = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
      if (!validTypes.includes(f.type)) {
        toast.error("Only PDF, DOC, and DOCX files are allowed");
        return;
      }
      if (f.size > 10 * 1024 * 1024) {
        toast.error("File size must be less than 10MB");
        return;
      }
      setFile(f);
      setUploadedResume(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
  });

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setProgress(0);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const { data } = await api.post<Resume>("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      clearInterval(progressInterval);
      setProgress(100);
      setUploadedResume(data);
      toast.success("Resume uploaded and parsed successfully!");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadedResume) return;
    setAnalyzing(true);
    try {
      const { data } = await api.post(`/analysis/${uploadedResume.id}`);
      toast.success("Analysis complete!");
      navigate(`/analysis/${data.id}`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Upload Resume</h1>
        <p className="text-[hsl(var(--muted-foreground))]">Upload your resume to get AI-powered analysis and ATS scoring.</p>
      </div>

      {/* Dropzone */}
      <Card>
        <CardContent className="p-8">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
              isDragActive
                ? "border-[hsl(var(--primary))] bg-[hsl(var(--primary)/0.05)]"
                : "border-[hsl(var(--border))] hover:border-[hsl(var(--primary)/0.5)] hover:bg-[hsl(var(--accent)/0.5)]"
            }`}
          >
            <input {...getInputProps()} />
            <motion.div initial={{ scale: 1 }} animate={{ scale: isDragActive ? 1.05 : 1 }} className="flex flex-col items-center gap-4">
              <div className="h-16 w-16 rounded-2xl gradient-primary flex items-center justify-center">
                <Upload className="h-8 w-8 text-white" />
              </div>
              {isDragActive ? (
                <p className="text-lg font-medium text-[hsl(var(--primary))]">Drop your resume here</p>
              ) : (
                <>
                  <p className="text-lg font-medium">Drag & drop your resume here</p>
                  <p className="text-sm text-[hsl(var(--muted-foreground))]">or click to browse — PDF, DOC, DOCX up to 10MB</p>
                </>
              )}
            </motion.div>
          </div>
        </CardContent>
      </Card>

      {/* Selected File */}
      {file && !uploadedResume && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-lg bg-[hsl(var(--primary)/0.1)] flex items-center justify-center">
                    <FileText className="h-5 w-5 text-[hsl(var(--primary))]" />
                  </div>
                  <div>
                    <p className="font-medium text-sm">{file.name}</p>
                    <p className="text-xs text-[hsl(var(--muted-foreground))]">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="icon" onClick={() => setFile(null)} disabled={uploading}>
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              {uploading && <Progress value={progress} className="mt-3" />}
              {!uploading && (
                <Button onClick={handleUpload} className="w-full mt-4 gap-2">
                  <Upload className="h-4 w-4" /> Upload & Parse
                </Button>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Uploaded Resume Preview */}
      {uploadedResume && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="border-green-500/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-600">
                <CheckCircle2 className="h-5 w-5" /> Resume Uploaded Successfully
              </CardTitle>
              <CardDescription>{uploadedResume.filename} • {formatFileSize(uploadedResume.file_size)}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Parsed Data Preview */}
              {uploadedResume.parsed_data && (
                <div className="grid gap-3 sm:grid-cols-2">
                  {uploadedResume.parsed_data.name && (
                    <div className="p-3 rounded-lg bg-[hsl(var(--accent))]">
                      <p className="text-xs text-[hsl(var(--muted-foreground))]">Name</p>
                      <p className="font-medium">{uploadedResume.parsed_data.name}</p>
                    </div>
                  )}
                  {uploadedResume.parsed_data.email && (
                    <div className="p-3 rounded-lg bg-[hsl(var(--accent))]">
                      <p className="text-xs text-[hsl(var(--muted-foreground))]">Email</p>
                      <p className="font-medium">{uploadedResume.parsed_data.email}</p>
                    </div>
                  )}
                  {uploadedResume.parsed_data.phone && (
                    <div className="p-3 rounded-lg bg-[hsl(var(--accent))]">
                      <p className="text-xs text-[hsl(var(--muted-foreground))]">Phone</p>
                      <p className="font-medium">{uploadedResume.parsed_data.phone}</p>
                    </div>
                  )}
                  {uploadedResume.parsed_data.skills?.length > 0 && (
                    <div className="p-3 rounded-lg bg-[hsl(var(--accent))] sm:col-span-2">
                      <p className="text-xs text-[hsl(var(--muted-foreground))] mb-2">Skills Detected</p>
                      <div className="flex flex-wrap gap-1.5">
                        {uploadedResume.parsed_data.skills.slice(0, 15).map((s, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-full bg-[hsl(var(--primary)/0.1)] text-[hsl(var(--primary))] text-xs font-medium">{s}</span>
                        ))}
                        {uploadedResume.parsed_data.skills.length > 15 && (
                          <span className="text-xs text-[hsl(var(--muted-foreground))]">+{uploadedResume.parsed_data.skills.length - 15} more</span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
              <Button onClick={handleAnalyze} className="w-full gap-2" disabled={analyzing}>
                {analyzing ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                Run AI Analysis & ATS Scoring
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
