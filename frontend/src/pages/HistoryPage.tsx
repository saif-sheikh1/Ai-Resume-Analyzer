import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { History, Search, Trash2, FileText, BarChart3, Download } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import api from "@/lib/api";
import type { AnalysisListItem } from "@/types";
import { formatDate, getScoreColor, getScoreLabel } from "@/lib/utils";
import { toast } from "sonner";

export default function HistoryPage() {
  const [analyses, setAnalyses] = useState<AnalysisListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "score">("date");

  useEffect(() => {
    const fetch = async () => {
      try {
        const { data } = await api.get<AnalysisListItem[]>("/analysis/");
        setAnalyses(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this analysis?")) return;
    try {
      await api.delete(`/analysis/${id}`);
      setAnalyses(analyses.filter((a) => a.id !== id));
      toast.success("Analysis deleted");
    } catch {
      toast.error("Delete failed");
    }
  };

  const handleDownloadPDF = async (id: string) => {
    try {
      const response = await api.get(`/reports/${id}/pdf`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `report_${id}.pdf`;
      a.click();
    } catch {
      toast.error("Download failed");
    }
  };

  const filtered = analyses
    .filter((a) => !search || a.resume_filename?.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === "score") return (b.ats_score || 0) - (a.ats_score || 0);
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Analysis History</h1>
          <p className="text-[hsl(var(--muted-foreground))]">{analyses.length} analyses</p>
        </div>
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[hsl(var(--muted-foreground))]" />
            <Input placeholder="Search resumes..." className="pl-9 w-64" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <select className="h-10 rounded-lg border border-[hsl(var(--input))] bg-[hsl(var(--background))] px-3 text-sm" value={sortBy} onChange={(e) => setSortBy(e.target.value as "date" | "score")}>
            <option value="date">Sort by Date</option>
            <option value="score">Sort by Score</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">{[1,2,3,4].map(i => <Skeleton key={i} className="h-20 w-full" />)}</div>
      ) : filtered.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <History className="h-12 w-12 mx-auto text-[hsl(var(--muted-foreground))] mb-4" />
            <p className="text-lg font-medium">No analyses yet</p>
            <p className="text-[hsl(var(--muted-foreground))] text-sm mb-4">Upload and analyze a resume to get started</p>
            <Link to="/upload"><Button>Upload Resume</Button></Link>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map((analysis, i) => (
            <motion.div key={analysis.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <Card className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between gap-4">
                    <Link to={`/analysis/${analysis.id}`} className="flex items-center gap-3 flex-1 min-w-0">
                      <div className="h-10 w-10 rounded-lg bg-[hsl(var(--primary)/0.1)] flex items-center justify-center flex-shrink-0">
                        <FileText className="h-5 w-5 text-[hsl(var(--primary))]" />
                      </div>
                      <div className="min-w-0">
                        <p className="font-medium text-sm truncate">{analysis.resume_filename || "Resume"}</p>
                        <p className="text-xs text-[hsl(var(--muted-foreground))]">{formatDate(analysis.created_at)}</p>
                      </div>
                    </Link>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <p className={`text-lg font-bold ${getScoreColor(analysis.ats_score || 0)}`}>{analysis.ats_score?.toFixed(0) || "—"}</p>
                        <p className="text-xs text-[hsl(var(--muted-foreground))]">{getScoreLabel(analysis.ats_score || 0)}</p>
                      </div>
                      <Button variant="ghost" size="icon" onClick={() => handleDownloadPDF(analysis.id)} title="Download PDF">
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => handleDelete(analysis.id)} title="Delete">
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
