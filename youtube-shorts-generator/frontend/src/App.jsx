import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Youtube, Scissors, Download, Upload, Play } from 'lucide-react'
import './App.css'

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [videoInfo, setVideoInfo] = useState(null)
  const [shorts, setShorts] = useState([])
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState('input') // input, processing, editing, upload

  const handleUrlSubmit = async () => {
    if (!youtubeUrl) return
    
    setLoading(true)
    try {
      const response = await fetch('/api/youtube/video-info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: youtubeUrl }),
      })
      
      const data = await response.json()
      if (response.ok) {
        setVideoInfo(data)
        setStep('processing')
      } else {
        alert('Erro ao obter informações do vídeo: ' + data.error)
      }
    } catch (error) {
      alert('Erro de conexão: ' + error.message)
    }
    setLoading(false)
  }

  const generateShorts = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/youtube/generate-shorts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          video_path: '/tmp/video.mp4', // Placeholder
          max_duration: 60 
        }),
      })
      
      const data = await response.json()
      if (response.ok) {
        setShorts(data.shorts)
        setStep('editing')
      } else {
        alert('Erro ao gerar shorts: ' + data.error)
      }
    } catch (error) {
      alert('Erro de conexão: ' + error.message)
    }
    setLoading(false)
  }

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
            <Youtube className="text-red-500" />
            YouTube to Shorts Generator
          </h1>
          <p className="text-gray-600">Transforme vídeos do YouTube em shorts virais para TikTok e YouTube Shorts</p>
        </div>

        {/* Step 1: URL Input */}
        {step === 'input' && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Youtube className="w-5 h-5" />
                Inserir URL do YouTube
              </CardTitle>
              <CardDescription>
                Cole o link do vídeo do YouTube que deseja transformar em shorts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Input
                  placeholder="https://www.youtube.com/watch?v=..."
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  className="flex-1"
                />
                <Button 
                  onClick={handleUrlSubmit} 
                  disabled={loading || !youtubeUrl}
                  className="px-6"
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    'Analisar'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Video Info & Processing */}
        {step === 'processing' && videoInfo && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Play className="w-5 h-5" />
                Informações do Vídeo
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <img 
                    src={videoInfo.thumbnail} 
                    alt={videoInfo.title}
                    className="w-full rounded-lg shadow-md"
                  />
                </div>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-lg">{videoInfo.title}</h3>
                    <p className="text-gray-600 text-sm mt-1">Por {videoInfo.uploader}</p>
                  </div>
                  <div className="flex gap-2 flex-wrap">
                    <Badge variant="secondary">
                      Duração: {formatDuration(videoInfo.duration)}
                    </Badge>
                    <Badge variant="secondary">
                      Visualizações: {videoInfo.view_count?.toLocaleString()}
                    </Badge>
                  </div>
                  <Button 
                    onClick={generateShorts}
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                        Gerando Shorts...
                      </>
                    ) : (
                      <>
                        <Scissors className="w-4 h-4 mr-2" />
                        Gerar Shorts
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Shorts Editing */}
        {step === 'editing' && shorts.length > 0 && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Scissors className="w-5 h-5" />
                  Shorts Gerados ({shorts.length})
                </CardTitle>
                <CardDescription>
                  Edite, pré-visualize e faça download dos seus shorts
                </CardDescription>
              </CardHeader>
            </Card>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {shorts.map((short, index) => (
                <Card key={short.id} className="overflow-hidden">
                  <CardContent className="p-4">
                    <div className="aspect-[9/16] bg-gray-100 rounded-lg mb-4 flex items-center justify-center">
                      <Play className="w-12 h-12 text-gray-400" />
                    </div>
                    <div className="space-y-2">
                      <h4 className="font-medium">{short.title}</h4>
                      <div className="flex justify-between text-sm text-gray-600">
                        <span>{formatDuration(short.start_time)} - {formatDuration(short.end_time)}</span>
                        <span>{formatDuration(short.duration)}</span>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline" className="flex-1">
                          <Play className="w-3 h-3 mr-1" />
                          Preview
                        </Button>
                        <Button size="sm" variant="outline" className="flex-1">
                          <Download className="w-3 h-3 mr-1" />
                          Download
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <Card>
              <CardContent className="p-6">
                <div className="flex gap-4 justify-center">
                  <Button className="px-8">
                    <Upload className="w-4 h-4 mr-2" />
                    Publicar no TikTok
                  </Button>
                  <Button variant="outline" className="px-8">
                    <Youtube className="w-4 h-4 mr-2" />
                    Publicar no YouTube
                  </Button>
                  <Button variant="outline" onClick={() => setStep('input')}>
                    Novo Vídeo
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

